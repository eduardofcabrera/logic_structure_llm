from problem_state import ProblemState

import re
import json

from typing import *
from pathlib import Path

import pddl.logic.predicates as pddl_predicates
import pddl.action as pddl_action
from pddl import parse_domain, parse_problem

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import HumanMessage, AIMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models.base import BaseChatModel
from langchain_core.runnables import Runnable


class Blocksworld:
    def __init__(
        self,
        config: Dict,
        model: BaseChatModel,
    ):
        self.config = config
        self.problem_state = self.create_problem_state()
        self.instance_prompt = self.get_instance_prompt()
        self.model = model

    def create_problem_state(self) -> ProblemState:

        domain_file = Path(self.config["domain_file"])
        instance_file = Path(self.config["instance_dir"]) / self.config[
            "instances_template"
        ].format(self.config["instance_id"])

        domain = parse_domain(domain_file)
        problem = parse_problem(instance_file)

        return ProblemState(domain=domain, problem=problem)

    def get_instance_prompt(self) -> Dict:

        with open(self.config["prompt_json_file"]) as f:
            instance_prompt = json.load(f)["instances"][self.config["instance_id"] - 2]
            f.close()

        return instance_prompt

    def reboot_problem_state(self) -> None:

        self.problem_state = self.create_problem_state()

    def text_to_action(self, text: str) -> Tuple[pddl_action.Action, Tuple[str]]:
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

    def take_action_from_text(self, text: str) -> Tuple[bool, bool]:

        action = self.text_to_action(text)
        if not action:
            return (False, False)
        return (self.problem_state.take_action(*action), True)

    def action_to_text(self, action: Tuple[pddl_action.Action, Tuple[str]]) -> str:
        actions_mapping = self.config["actions"]
        encoded_parameters = self.config["encoded_objects"]

        return actions_mapping[action[0].name].format(
            *[encoded_parameters[parameter] for parameter in action[-1]]
        )

    def predicate_to_text(self, predicate: pddl_predicates.Predicate) -> str:
        predicates_mapping = self.config["predicates"]
        encoded_parameters = self.config["encoded_objects"]

        return predicates_mapping[predicate.name].format(
            *[encoded_parameters[term.name] for term in predicate.terms]
        )

    def current_state_to_text(self) -> str:
        current_state_predicate_list = self.problem_state.current_state_predicate_list

        predicates_texts = [
            self.predicate_to_text(predicate)
            for predicate in current_state_predicate_list
        ]

        state_text = (
            "As current conditions I have that " + ", ".join(predicates_texts) + ".\n"
        )

        return state_text

    def goal_to_text(self) -> str:

        goal_precondition = self.problem_state.goal

        if isinstance(goal_precondition, pddl_predicates.Predicate):
            predicates_texts = [
                self.predicate_to_text(goal_precondition).replace(" is", "")
            ]
        else:
            predicates_texts = [
                self.predicate_to_text(predicate).replace(" is", "")
                for predicate in goal_precondition.operands
            ]

        goal_text = "My goal is to have " + " and ".join(predicates_texts) + ".\n"

        return goal_text

    def possible_actions_to_text(self) -> str:
        possible_actions = self.problem_state.get_all_possible_actions()
        actions_texts = [self.action_to_text(action) for action in possible_actions]

        possible_actions_text = "Possible actions:\n"
        for i, action_text in enumerate(actions_texts):
            possible_actions_text += f"{i+1}: {action_text}\n"

        return possible_actions_text


class BlocksworldOnlyPrompt(Blocksworld):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

    def get_chain(self) -> Runnable:
        model = self.model
        str_output_parser = StrOutputParser()
        prompt = PromptTemplate.from_template(
            "{input}" + self.config["prompts"]["order_prompts"]["only_prompt"]
        )
        chain = prompt | model | str_output_parser

        return chain

    def start_inference(self) -> Tuple[bool, str, Dict[str : Tuple[str, bool]]]:

        chain = self.get_chain()

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


class BlocksworldChat(Blocksworld):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

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

    def get_action_return_prompt(
        self, action_return: bool, with_current_state_prompt: bool = False
    ) -> str:

        feedback = "positive" if action_return else "negative"
        state_text = self.current_state_to_text() if with_current_state_prompt else ""

        feedback_prompt = self.config["prompts"]["feedback_prompts"][feedback]
        order_prompt = self.config["prompts"]["order_prompts"][feedback]

        return feedback_prompt + state_text + order_prompt

    def get_chain(self) -> Runnable:
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

    def chat_iteration(
        self, prompt_input: str, chat_history: List[BaseMessage], chat_chain: Runnable
    ) -> Tuple[str, List[BaseMessage]]:
        model_return = chat_chain.invoke(
            {"input": prompt_input, "chat_history": chat_history}
        )

        chat_history.append(HumanMessage(content=prompt_input))
        chat_history.append(AIMessage(content=model_return))

        return model_return, chat_history

    def get_chat_content_from_chat_history(
        self, chat_history: List[BaseMessage]
    ) -> str:
        chat_text = [f"{message.type}: {message.content}" for message in chat_history]
        chat_text = "\n".join(chat_text)
        return chat_text

    def start_inference(
        self, with_current_state_prompt: bool = False
    ) -> Tuple[bool, str, Dict[str : Tuple[str, bool]]]:

        chat_chain = self.get_chain()

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


class BlocksworldChatWithPossibleActions(Blocksworld):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

    def get_chain(self) -> Runnable:
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

    def get_first_prompt(self) -> str:

        current_condition_text = self.current_state_to_text()
        goal_text = self.goal_to_text()
        possible_actions_text = self.possible_actions_to_text()

        order_prompt = "\nReturn the number of the next action to achieve my goal. Return only: <ACTION_NUMBER>"

        first_prompt = (
            self.config["domain_intro"]
            + self.config["one_shot_chat_with_possible_actions"]
            + "\n[STATEMENT]\n"
            + current_condition_text
            + goal_text
            + "\n[NEXT ACTION]\n"
            + possible_actions_text
            + order_prompt
        )

        return first_prompt

    def get_prompt(self) -> str:
        current_condition_text = self.current_state_to_text()
        goal_text = self.goal_to_text()
        possible_actions_text = self.possible_actions_to_text()

        order_prompt = "\nReturn the number of the next action to achieve my goal. Return only: <ACTION_NUMBER>"

        prompt = (
            # "\n[STATEMENT]\n"
            # + current_condition_text
            # + goal_text
            "Action Realized! Goal not achieved yet! \n[NEXT ACTION]\n"
            + possible_actions_text
            + order_prompt
        )

        return prompt

    def chat_iteration(
        self, prompt_input: str, chat_history: List[BaseMessage], chat_chain: Runnable
    ) -> Tuple[str, List[BaseMessage]]:
        model_return = chat_chain.invoke(
            {"input": prompt_input, "chat_history": chat_history}
        )

        chat_history.append(HumanMessage(content=prompt_input))
        chat_history.append(AIMessage(content=model_return))

        return model_return, chat_history

    def get_chat_content_from_chat_history(
        self, chat_history: List[BaseMessage]
    ) -> str:
        chat_text = [f"{message.type}: {message.content}" for message in chat_history]
        chat_text = "\n".join(chat_text)
        return chat_text

    def start_inference(self) -> Tuple[bool, str, List[str]]:

        chain = self.get_chain()

        chat_history = []
        actions = []

        first_prompt = self.get_first_prompt()
        model_return, chat_history = self.chat_iteration(
            first_prompt, chat_history, chain
        )

        for _ in range(self.config["max_iterations"]):

            try:
                action_id = int(model_return) - 1
            except:
                print(model_return)
                break
            possible_actions = self.problem_state.get_all_possible_actions()
            action = possible_actions[action_id]
            self.problem_state.take_action(*action)
            actions.append(self.action_to_text(action))

            if self.problem_state.goal_reached():
                break

            prompt = self.get_prompt()
            model_return, chat_history = self.chat_iteration(
                prompt, chat_history, chain
            )

        goal_reached = self.problem_state.goal_reached()
        self.reboot_problem_state()

        chat_history_text = self.get_chat_content_from_chat_history(chat_history)

        return goal_reached, chat_history_text, actions
