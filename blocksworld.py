from problem_state import ProblemState

from pddl import parse_domain, parse_problem

import yaml
import re
import json

from pathlib import Path
from tqdm import tqdm

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.chat_models.base import BaseChatModel


class Blocksworld:
    def __init__(
        self,
        config: dict,
        model: BaseChatModel,
    ):
        self.config = config
        self.problem_state = self.create_problem_state()
        self.instance_prompt = self.get_instance_prompt()
        self.model = model

    def create_problem_state(self):

        domain_file = Path(self.config["domain_file"])
        instance_file = Path(self.config["instance_dir"]) / self.config[
            "instances_template"
        ].format(self.config["instance_id"])

        domain = parse_domain(domain_file)
        problem = parse_problem(instance_file)

        return ProblemState(domain=domain, problem=problem)

    def get_instance_prompt(self):

        with open(self.config["prompt_json_file"]) as f:
            instance_prompt = json.load(f)["instances"][self.config["instance_id"] - 2]
            f.close()

        return instance_prompt

    def reboot_problem_state(self):

        self.problem_state = self.create_problem_state()

    def text_to_action(self, text: str) -> tuple:
        actions_text_mapping = self.config["actions"]
        encoded_parameters = self.config["encoded_objects"]

        actions_text_match = {
            action_name: re.match(action_text_format.replace("{}", "(.*)"), text)
            for action_name, action_text_format in actions_text_mapping.items()
        }

        action_match = [
            action_name
            for action_name, action_text_match in actions_text_match.items()
            if action_text_match
        ]

        if len(action_match) != 1:
            return

        action_name = action_match[0]
        action_text_match = actions_text_match[action_name]

        parameters = action_text_match.groups()

        encoded_parameters_values = list(encoded_parameters.values())
        encoded_parameters_keys = list(encoded_parameters.keys())

        parameters = tuple(
            (
                encoded_parameters_keys[encoded_parameters_values.index(parameter)]
                for parameter in parameters
            )
        )

        actions = self.problem_state.actions
        action = [action for action in actions if action.name == action_name][0]

        return action, parameters

    def take_action_from_text(self, text: str):

        action = self.text_to_action(text)
        if not action:
            return (False, False)
        return (self.problem_state.take_action(*action), True)

    def current_state_to_text(self):
        current_state_predicate_list = self.problem_state.current_state_predicate_list
        predicates_mapping = self.config["predicates"]
        encoded_parameters = self.config["encoded_objects"]

        predicates_texts = [
            predicates_mapping[predicate.name].format(
                *[encoded_parameters[term.name] for term in predicate.terms]
            )
            for predicate in current_state_predicate_list
        ]

        state_text = (
            "As current conditions I have that " + ", ".join(predicates_texts) + ".\n"
        )

        return state_text

    def get_first_prompt(self) -> str:

        remove_string = self.config["prompts"]["remove_string"]
        len_remove_string = len(remove_string)
        query = self.instance_prompt["query"].split("[STATEMENT]")[-1][
            :-len_remove_string
        ]

        first_prompt = (
            self.config["domain_intro"]
            + self.config["one_shot_chat"]
            + self.config["one_shot_chat_2"]
            + "\n[STATEMENT]"
            + query
            + self.config["prompts"]["order_prompts"]["first_prompt"]
        )

        return first_prompt

    def get_only_prompt_chain(self):
        model = self.model
        str_output_parser = StrOutputParser()
        prompt = PromptTemplate.from_template(
            "{input}" + self.config["prompts"]["order_prompts"]["only_prompt"]
        )
        chain = prompt | model | str_output_parser

        return chain

    def start_chat_only_prompt(self):

        chain = self.get_only_prompt_chain()

        _input = self.instance_prompt["query"]
        model_return = chain.invoke({"input": _input})

        actions = model_return.split("\n")
        actions = {
            f"{i}": (action, self.take_action_from_text(action)[0])
            for i, action in enumerate(actions)
        }

        goal_reached = self.problem_state.goal_reached()

        self.reboot_problem_state()

        return goal_reached, _input + model_return, actions

    def get_action_return_prompt(
        self, action_return: bool, with_current_state_prompt: bool = False
    ) -> str:

        feedback = "positive" if action_return else "negative"
        state_text = self.current_state_to_text() if with_current_state_prompt else ""

        feedback_prompt = self.config["prompts"]["feedback_prompts"][feedback]
        order_prompt = self.config["prompts"]["order_prompts"][feedback]

        return feedback_prompt + state_text + order_prompt

    def get_chat_chain(self):
        model = self.model
        str_output_parser = StrOutputParser()
        prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
            ]
        )

        chat_chain = prompt | model | str_output_parser
        return chat_chain

    def chat_iteration(self, prompt_input: str, chat_history: list, chat_chain):
        model_return = chat_chain.invoke(
            {"input": prompt_input, "chat_history": chat_history}
        )

        chat_history.append(HumanMessage(content=prompt_input))
        chat_history.append(AIMessage(content=model_return))

        return model_return, chat_history

    def get_chat_content_from_chat_history(self, chat_history: list) -> str:
        chat_text = [f"{message.type}: {message.content}" for message in chat_history]
        chat_text = "\n".join(chat_text)
        return chat_text

    def start_chat(self, with_current_state_prompt: bool = False):

        chat_chain = self.get_chat_chain()

        chat_history = []
        actions = []

        first_prompt_text = self.get_first_prompt()

        model_return, chat_history = self.chat_iteration(
            first_prompt_text, chat_history, chat_chain
        )

        for _ in range(self.config["max_iterations"]):

            action_return, is_action = self.take_action_from_text(model_return)
            prompt_text = self.get_action_return_prompt(
                action_return, with_current_state_prompt
            )

            if not (is_action):
                break

            actions.append((model_return, action_return))

            if self.problem_state.goal_reached():
                break

            model_return, chat_history = self.chat_iteration(
                prompt_text, chat_history, chat_chain
            )

        actions = {f"{i}": action for i, action in enumerate(actions)}
        chat_text = self.get_chat_content_from_chat_history(chat_history)

        goal_reached = self.problem_state.goal_reached()

        self.reboot_problem_state()

        return goal_reached, chat_text, actions


def main(instance_id: int):

    with open("configs/blocksworld.yaml") as f:
        config = yaml.safe_load(f)
        f.close()

    domain = parse_domain("data/pddlgenerators/blocksworld/4ops/domain.pddl")
    problem = parse_problem(
        f"data/instances/blocksworld/generated_basic/instance-{instance_id}.pddl"
    )

    with open("data/prompts/blocksworld/task_1_plan_generation.json") as f:
        instance_prompt = json.load(f)["instances"][instance_id - 2]
        f.close()

    problem_state = ProblemState(domain=domain, problem=problem)

    model = ChatOpenAI(model="gpt-4-0125-preview")

    blocksworld_run = Blocksworld(
        problem_state=problem_state,
        config=config,
        instance_prompt=instance_prompt,
        model=model,
    )

    returns_only_prompt = blocksworld_run.start_chat_only_prompt()
    returns_chat = blocksworld_run.start_chat()

    return (returns_only_prompt, returns_chat)


if __name__ == "__main__":

    returns = []

    for instance_id in tqdm(range(2, 13)):
        returns.append(main(instance_id))

    print(returns)

    json_out = {
        i: {
            "only_prompt": {
                "goal_achieved": _return[0][0],
                "content": _return[0][1],
                "actions": _return[0][2],
            },
            "chat": {"goal_achieved": _return[1][0], "content": _return[1][1]},
        }
        for i, _return in enumerate(returns)
    }

    with open("json_out.json", "w") as f:
        json.dump(json_out, f)
