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


def is_valid_action(action_text: str, config: Dict):
    actions_text_mapping = config["actions"]

    actions_text_match = {
        action_name: re.match(action_text_format.replace("{}", "(.*)"), action_text)
        for action_name, action_text_format in actions_text_mapping.items()
    }

    action_match = [
        action_name
        for action_name, action_text_match in actions_text_match.items()
        if action_text_match
    ]

    if len(action_match) != 1:
        return False
    return True
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

        encoded_parameters_values = list(encoded_parameters.values())
        encoded_parameters_keys = list(encoded_parameters.keys())
        
        parameters = action_text_match.groups()
        parameters_check = [parameter in encoded_parameters_values for parameter in parameters]
        if False in parameters_check:
            return

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
            "{input}" + self.config["prompts"]["order_prompts"]
        )
        chain = prompt | model | str_output_parser

        return chain

    def start_inference(self) -> Tuple[bool, str, Dict[str, Tuple[str, bool]]]:

        chain = self.get_chain()

        _input = self.instance_prompt["query"]
        input_split = "My plan is as follows:".join(_input.split("My plan is as follows:")[:-1])
        order_prompt = """Return the plan that makes me achieve my goal.\n Write only:\n ```<plan>\n[PLAN]\n<\plan>``` """
        
        _input = input_split + order_prompt
        
        model_return = chain.invoke({"input": _input})
        
        #try:
        #    actions = model_return.lower().split("<plan>")[1].split("<\plan>")[0].split("\n")
        #except:
        #    print(model_return)
        #    return False, _input + model_return, []
        #actions = [action for action in actions if action != ""]

        actions = model_return.split("\n")
        actions = {
            f"{i}": (action, self.take_action_from_text(action))
            for i, action in enumerate(actions)
        }
        
        actions = {
            key: (value[0], value[1][0])
            for key, value in actions.items() if value[1][1]
        }

        goal_reached = self.problem_state.goal_reached()

        self.reboot_problem_state()

        return goal_reached, _input + model_return, actions
    
class BlocksworldOnlyPromptIterative(Blocksworld):
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
        
        chain = prompt | model | str_output_parser
        return chain
       
    def get_chat_content_from_chat_history(
        self, chat_history: List[BaseMessage]
    ) -> str:
        chat_text = [f"{message.type}: {message.content}" for message in chat_history]
        chat_text = "\n".join(chat_text)
        return chat_text
    
    def chat_iteration(
        self, prompt_input: str, chat_history: List[BaseMessage], chat_chain: Runnable
    ) -> Tuple[str, List[BaseMessage]]:
        model_return = chat_chain.invoke(
            {"input": prompt_input, "chat_history": chat_history}
        )

        chat_history.append(HumanMessage(content=prompt_input))
        chat_history.append(AIMessage(content=model_return))

        return model_return, chat_history

    def start_inference(self) -> Tuple[bool, str, Dict[str, Tuple[str, bool]]]:

        chain = self.get_chain()
        chat_history = []

        _input = self.instance_prompt["query"]
        input_split = "My plan is as follows:".join(_input.split("My plan is as follows:")[:-1])
        order_prompt = """Return the plan that makes me achieve my goal.\n Write only:\n ```<plan>\n[PLAN]\n<\plan>``` """
        
        _input = input_split + order_prompt
        
        model_return, chat_history = self.chat_iteration(_input, chat_history, chain)
        #model_return = chain.invoke({"input": _input})
        
        for _ in range(self.config["max_iterations"]):
            
            actions = model_return.split("\n")
            actions = {
                f"{i}": (action, self.take_action_from_text(action))
                for i, action in enumerate(actions)
            }
            
            actions = {
                key: (value[0], value[1][0])
                for key, value in actions.items() if value[1][1]
            }

            goal_reached = self.problem_state.goal_reached()
            if goal_reached:
                break
            
            prompt = "The previous plan was incorrect please correct it and write it again. Return the plan that makes me achieve my goal.\n Write only:\n ```<plan>\n[PLAN]\n<\plan>``` \n"
            model_return, chat_history = self.chat_iteration(prompt, chat_history, chain)
            self.reboot_problem_state()

        chat_content = self.get_chat_content_from_chat_history(chat_history)
        self.reboot_problem_state()

        return goal_reached, chat_content, actions


class BlocksworldChat(Blocksworld):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

    def get_few_shot_text(self) -> str:
        few_shot_text = ""
        for n_shot in range(self.config["few_shot"]):
            few_shot_text += "\n" + self.config[f"few_shot_example_{n_shot+1}_"]
        return few_shot_text

    def get_first_prompt(self) -> str:

        current_condition_text = self.current_state_to_text()
        goal_text = self.goal_to_text()
        few_shot_text = self.get_few_shot_text()
        
        order_prompt = "\nReturn the next action to achieve my goal. Return one, and only one, action, without nothing more.\nWrite only with:\n```THE NEXT BEST ACTION IS: <action>.```"

        first_prompt = (
            self.config["domain_intro"]
            + few_shot_text
            + "\n[STATEMENT]\n"
            + current_condition_text
            + goal_text
            #+ order_prompt
            + self.config["prompts"]["order_prompts"]["first_prompt"]
        )

        return first_prompt

    def get_action_return_prompt(
        self, action_return: bool, with_current_state_prompt: bool = False
    ) -> str:

        feedback = "positive" if action_return else "negative"
        state_text = self.current_state_to_text() if with_current_state_prompt else ""

        feedback_prompt = self.config["prompts"]["feedback_prompts"][feedback]
        #feedback_prompt = ""
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
    ) -> Tuple[bool, str, Dict[str, Tuple[str, bool]]]:

        chat_chain = self.get_chain()

        chat_history = []
        actions = []

        first_prompt_text = self.get_first_prompt()
        model_return, chat_history = self.chat_iteration(
            first_prompt_text, chat_history, chat_chain
        )

        for _ in range(self.config["max_iterations"]):
            
            index = model_return.find("THE NEXT BEST ACTION IS: ")
            if index == -1:
                action = "no action"
            else:
                try:
                    action = model_return.split("THE NEXT BEST ACTION IS: ")[-1].lower()
                    action = action.split(".")[0]
                except:
                    action = "no action"
            
            action_return, is_action = self.take_action_from_text(action)
            actions.append((action, action_return))

            if not (is_action):
                break

            if self.problem_state.goal_reached():
                break

            prompt_text = self.get_action_return_prompt(
                action_return, with_current_state_prompt
            )

            model_return, chat_history = self.chat_iteration(
                prompt_text, chat_history, chat_chain
            )

        actions = {f"{i}": action for i, action in enumerate(actions)}
        chat_text = self.get_chat_content_from_chat_history(chat_history)

        goal_reached = self.problem_state.goal_reached()

        self.reboot_problem_state()

        return goal_reached, chat_text, actions


class BlocksworldChatWithPossibleActions(BlocksworldChat):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

    def get_first_prompt(self) -> str:

        current_condition_text = self.current_state_to_text()
        goal_text = self.goal_to_text()
        possible_actions_text = self.possible_actions_to_text()
        few_shot_text = self.get_few_shot_text()
        order_prompt = self.config["prompts"]["order_prompts"]
        
        order_prompt = """\nReturn the number of the best next action to achieve my goal. Write only with:\n```RETURN: <OPTION NUMBER>.```"""

        first_prompt = (
            self.config["domain_intro"]
            + few_shot_text
            + "\n[STATEMENT]\n"
            + current_condition_text
            + goal_text
            #+ "\nSequence of actions already taken to achieve my goal:\nno actions\n"
            + "\n[NEXT ACTION]\n"
            + possible_actions_text
            + order_prompt
        )

        return first_prompt

    def get_prompt(self) -> str:
        current_condition_text = self.current_state_to_text()
        goal_text = self.goal_to_text()
        possible_actions_text = self.possible_actions_to_text()
        order_prompt = self.config["prompts"]["order_prompts"]

        actions_taken = self.problem_state.actions_taken
        actions_taken_text = "\nSequence of actions already taken to achieve my goal:\n"
        for action in actions_taken:
            action_text = self.action_to_text(action)
            actions_taken_text += action_text + "\n"
            
        order_prompt = """\nReturn the number of the best next action to achieve my goal. Write only with:\n```RETURN: <OPTION NUMBER>.```"""

        prompt = (
            #"Action Realized!\n"
            #+ "\nGoal not achieved yet!\n"
            "[STATEMENT]\n"
            + current_condition_text
            + goal_text
            #+ actions_taken_text
            + "\n[NEXT ACTION]\n"
            + possible_actions_text
            + order_prompt
        )

        return prompt

    def start_inference(self) -> Tuple[bool, str, List[str]]:

        chain = self.get_chain()

        chat_history = []
        actions = []

        first_prompt = self.get_first_prompt()
        model_return, chat_history = self.chat_iteration(
            first_prompt, chat_history, chain
        )

        #chat_history[0].content = chat_history[0].content.split("[STATEMENT]")[0]
        #chat_history = chat_history[:1]
        
        #prompt = "I am playing with a set of blocks where I need to arrange the blocks into stacks. Here are the actions I can do\n\nPick up a block\nUnstack a block from on top of another block\nPut down a block\nStack a block on top of another block\n\nI have the following restrictions on my actions:\nI can only pick up or unstack one block at a time.\nI can only pick up or unstack a block if my hand is empty.\nI can only pick up a block if the block is on the table and the block is clear. A block is clear if the block has no other blocks on top of it and if the block is not picked up.\nI can only unstack a block from on top of another block if the block I am unstacking was really on top of the other block.\nI can only unstack a block from on top of another block if the block I am unstacking is clear.\nOnce I pick up or unstack a block, I am holding the block.\nI can only put down a block that I am holding.\nI can only stack a block on top of another block if I am holding the block being stacked.\nI can only stack a block on top of another block if the block onto which I am stacking the block is clear.\nOnce I put down or stack a block, my hand becomes empty.\nOnce you stack a block on top of a second block, the second block is no longer clear.\n\nBelow is an example to help you achieve my goal.\n[STATEMENT]\nAs current conditions I have that the orange block is on the table, the orange block is clear, the hand is empty, the\nblue block is clear, the red block is clear, the blue block is on the table, the red block is on the table.\nMy goal is to have the red block on top of the orange block and the blue block on top of the red block.\n\nSequence of actions to achieve my goal:\npick up the red block\nstack the red block on top of the orange block\npick up the blue block\nstack the blue block on top of the red block\nGoal Achieved!\n\nBelow is an example to help you achieve my goal.\n[STATEMENT]\nAs current conditions I have that, the orange block is clear, the hand is empty, the blue block is on top of the red block, the orange block is on top of the blue block and the red block is on the table.\nMy goal is to have that the red block is on top of the blue block and the orange block is on top of the red block.\n\nSequence of actions to achieve my goal:\nunstack the orange block from on top of the blue block\nput down the orange block\nunstack the blue block from on top of the red block\nput down the blue block\npick up the red block\nstack the red block on top of the blue block\npick up the orange block\nstack the orange block on top of the red block\\\nGoal Achieved!\n\n[STATEMENT]\nAs current conditions I have that the blue block is clear, the blue block is on top of the red block, the orange block is clear, the red block is on the table, the hand is empty, the orange block is on the table.\nMy goal is to have the red block on top of the blue block and the orange block on top of the red block.\n\n[NEXT ACTION]\nPossible actions:\n1: unstack the blue block from on top of the red block\n2: pick up the orange block\nReturn the number of the best next action to achieve my goal. Explain your decision and then write: [ACTION NUMBER]: <ACTION_NUMBER>\n"
        prompt = ""
        for _ in range(self.config["max_iterations"]):
            
            model_return = model_return.lower()
        
            index = model_return.find("return")
            if index == -1:
                print(model_return)
                break
            else:
                index = index + len("return") + 2
                option_str = model_return[index]
                try:
                    option_int = int(option_str) - 1
                except:
                    print(model_return)
                    break

            """index = model_return.find("[ACTION NUMBER]")
            if index == -1:
                print(model_return)
                break
            action_srt = model_return[index + len("[ACTION NUMBER]") + 2]"""
            """try:
                action_id = int(model_return) - 1
            except:
                print(model_return)
                break"""
            possible_actions = self.problem_state.get_all_possible_actions()
            if option_int >= len(possible_actions):
                print(model_return)
                break
            action = possible_actions[option_int]
            self.problem_state.take_action(*action)
            actions.append(self.action_to_text(action))

            if self.problem_state.goal_reached():
                break

            prompt = self.get_prompt()
            model_return, chat_history = self.chat_iteration(
                prompt, chat_history, chain
            )

            chat_history = chat_history[:1]

        goal_reached = self.problem_state.goal_reached()
        self.reboot_problem_state()
        
        chat_history.append(HumanMessage(content=prompt))
        chat_history.append(AIMessage(content=model_return))

        chat_history_text = self.get_chat_content_from_chat_history(chat_history)

        return goal_reached, chat_history_text, actions
