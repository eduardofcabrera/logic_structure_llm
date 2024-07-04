from typing import *
from problem_state import ProblemState

import re
import json
import random

from typing import *
from pathlib import Path
from abc import abstractmethod

import pddl.logic.predicates as pddl_predicates
import pddl.action as pddl_action
from pddl import parse_domain, parse_problem

from langchain.schema import BaseMessage
from langchain.chat_models.base import BaseChatModel


class Blocksworld:
    def __init__(
        self,
        config: Dict,
        model: BaseChatModel = None,
    ):
        self.config = config
        self.problem_state = self.create_problem_state()
        self.model = lambda: model

    def create_problem_state(self) -> ProblemState:

        domain_file = Path(self.config["domain_file"])
        instance_file = self.config["pddl_file"]

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

    def filter_text_action(self, text: str) -> str:
        actions_text_mapping = self.config["actions"]
        text = text.lower()
        sort_check = ["unstack", "putdown", "stack", "pickup"]
        for action in sort_check:
            mapping = actions_text_mapping[action]
            mapping = "(.*)" + mapping.replace("{}", "(.*)")
            match_obj = re.match(mapping, text)
            if match_obj:
                break
        if match_obj == None:
            return text
        cut_index_init = match_obj.regs[1][1]
        filtered_text = text[cut_index_init:]
        n_blocks = 1 if action in ["putdown", "pickup"] else 2
        filtered_text = "block".join(filtered_text.split("block")[:n_blocks]) + "block"
        return filtered_text

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
        parameters = [parameter.replace("the ", "") for parameter in parameters]
        parameters_check = [
            parameter in encoded_parameters_values for parameter in parameters
        ]
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

    def get_one_shot_text(self) -> str:
        if self.config["one_shot"]:
            prompt = self.instance_prompt["query"].split("[STATEMENT]")[1]
            return "[STATEMETN]\n" + prompt + "\nAnswer based on the example above.\n"
        return ""

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

        predicates_texts.sort()

        # random.seed(50)
        # random.shuffle(predicates_texts)

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

        # random.seed(50)
        # random.shuffle(predicates_texts)

        # predicates_texts = predicates_texts[::-1]
        predicates_texts.sort()
        goal_text = "My goal is to have " + " and ".join(predicates_texts) + ".\n"

        return goal_text

    def possible_actions_to_text(self, possible_actions=None) -> str:
        if not possible_actions:
            possible_actions = self.problem_state.get_all_possible_actions()
        actions_texts = [self.action_to_text(action) for action in possible_actions]
        # actions_texts.sort()

        possible_actions_text = "Possible actions:\n"
        for i, action_text in enumerate(actions_texts):
            possible_actions_text += f"{i+1}: {action_text}\n"

        return possible_actions_text

    def get_chat_content_from_chat_history(
        self, chat_history: List[BaseMessage]
    ) -> str:
        chat_text = [f"{message.type}: {message.content}" for message in chat_history]
        chat_text = "\n".join(chat_text)
        return chat_text

    def get_state(self):
        possible_actions = self.problem_state.get_all_possible_actions()
        possible_actions_text = [
            self.action_to_text(action) for action in possible_actions
        ]
        possible_actions_dict = {
            self.action_to_text(possible_action): possible_action
            for possible_action in possible_actions
        }
        possible_actions = list(dict(sorted(possible_actions_dict.items())).values())
        possible_actions_text.sort()
        return (
            self.current_state_to_text(),
            possible_actions,
            possible_actions_text,
            self.goal_to_text(),
        )


if __name__ == "__main__":
    pass
