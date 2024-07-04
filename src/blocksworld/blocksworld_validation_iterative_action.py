from problem_state import ProblemState
import random

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

from src.blocksworld.blocksworld import Blocksworld

from src.blocksworld.utils import is_valid_action


class BlocksworldChat(Blocksworld):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

    def get_chain(self) -> Runnable:
        model = self.model()
        str_output_parser = StrOutputParser()
        prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
            ]
        )

        chat_chain = prompt | model | str_output_parser
        return chat_chain

    def model_return_parser(self, model_return: str) -> str:

        actions = model_return.split("\n")
        actions = [self.filter_text_action(action) for action in actions]

        actions = [action for action in actions if is_valid_action(action, self.config)]

        if len(actions) == 0:
            return "no action"

        return actions[0]

        index = model_return.find("THE NEXT BEST ACTION IS: ")
        if index == -1:
            action = "no action"
        else:
            try:
                action = self.filter_text_action(model_return)
            except:
                action = "no action"
        return action

    def update_chat_history(self, chat_history: List, prompt: str, action: str) -> List:
        chat_history.append(HumanMessage(content=prompt))
        # chat_history.append(AIMessage(content="THE NEXT BEST ACTION IS: " + action))
        chat_history.append(AIMessage(content=action))
        return chat_history

    def get_prompt(
        self, chat_history: List, actions: List, current_state: str, goal: str
    ) -> str:

        cot_prompt = "\n\n[STATEMENT]\nAs initial conditions I have that, the red block is clear, the blue block is clear, the yellow block is clear, the hand is empty, the blue block is on top of the orange block, the red block is on the table, the orange block is on the table and the yellow block is on the table\nMy goal is to have that the orange block is on top of the blue block.\nMy plan is as follows:\n\n[PLAN]\n1. Current State: the red block is clear, the blue block is clear, the yellow block is clear, the hand is empty, the blue block is on top of the orange block, the red block is on the table, the orange block is on the table and the yellow block is on the table\n   Action: unstack the blue block from on top of the orange block\n   Reason: The above action is applicable in the current state because its preconditions; the blue block is clear, the hand is empty and the blue block is on top of the orange block, are satisfied in the current state.\n   Resulting State: the red block is clear, the orange block is clear, the yellow block is clear, the hand is currently holding blue block, the red block is on the table, the orange block is on the table and the yellow block is on the table\n\n2. Current State: the red block is clear, the orange block is clear, the yellow block is clear, the hand is currently holding blue block, the red block is on the table, the orange block is on the table and the yellow block is on the table\n   Action: put down the blue block\n   Reason: The above action is applicable in the current state because its preconditions; the hand is currently holding blue block, are satisfied in the current state.\n   Resulting State: the red block is clear, the blue block is clear, the orange block is clear, the yellow block is clear, the hand is empty, the red block is on the table, the blue block is on the table, the orange block is on the table and the yellow block is on the table\n\n3. Current State: the red block is clear, the blue block is clear, the orange block is clear, the yellow block is clear, the hand is empty, the red block is on the table, the blue block is on the table, the orange block is on the table and the yellow block is on the table\n   Action: pick up the orange block\n   Reason: The above action is applicable in the current state because its preconditions; the orange block is clear, the hand is empty and the orange block is on the table, are satisfied in the current state.\n   Resulting State: the red block is clear, the blue block is clear, the yellow block is clear, the hand is currently holding orange block, the red block is on the table, the blue block is on the table and the yellow block is on the table\n\n4. Current State: the red block is clear, the blue block is clear, the yellow block is clear, the hand is currently holding orange block, the red block is on the table, the blue block is on the table and the yellow block is on the table\n   Action: stack the orange block on top of the blue block\n   Reason: The above action is applicable in the current state because its preconditions; the blue block is clear and the hand is currently holding orange block, are satisfied in the current state.\n   Resulting State: the red block is clear, the orange block is clear, the yellow block is clear, the hand is empty, the orange block is on top of the blue block, the red block is on the table, the blue block is on the table and the yellow block is on the table\n\nFinal State: the red block is clear, the orange block is clear, the yellow block is clear, the hand is empty, the orange block is on top of the blue block, the red block is on the table, the blue block is on the table and the yellow block is on the table\nThe goal conditions are satisfied in the final state. Hence, the above plan is valid.\n[PLAN END]\n\n"
        request_prompt = "\nReturn the next best action to take as the example above.\n"

        if len(chat_history) == 0:
            few_shot_text = self.get_one_shot_text()
            prompt = (
                self.config["domain_intro"]
                + cot_prompt
                + "\n[STATEMENT]\n"
                + current_state
                + goal
                + request_prompt
                # + self.config["prompts"]["order_prompts"]["first_prompt"]
            )
        else:
            feedback_positive = actions[-1][-1]
            feedback = "positive" if feedback_positive else "negative"

            feedback_prompt = self.config["prompts"]["feedback_prompts"][feedback]
            order_prompt = self.config["prompts"]["order_prompts"][feedback]

            order_prompt = request_prompt

            prompt = feedback_prompt + order_prompt

        return prompt

    def state_transition(self, chat_history: List, actions: List, chain: Runnable):

        current_state, _, _, goal = self.get_state()
        prompt = self.get_prompt(chat_history, actions, current_state, goal)

        model_return = chain.invoke({"input": prompt, "chat_history": chat_history})
        returned_action = self.model_return_parser(model_return)
        try:
            is_possible_action, is_action = self.take_action_from_text(returned_action)
        except:
            is_possible_action, is_action = False, False
        action_taken = (returned_action, is_possible_action, is_action)

        chat_history = self.update_chat_history(chat_history, prompt, model_return)

        return chat_history, action_taken

    def update_pbar(self, pbar, i):
        if pbar:
            pbar.set_description(f"Iteration: {i+1}/{self.config['max_iterations']}")

    def start_inference(self, pbar=None):

        chat_history = []
        actions = []
        chain = self.get_chain()

        for i in range(self.config["max_iterations"]):
            self.update_pbar(pbar, i)

            chat_history, action_taken = self.state_transition(
                chat_history, actions, chain
            )
            # if not action_taken[-1]: # is not an action
            #    break
            actions.append(
                (action_taken[0], action_taken[1])
            )  # action name and is_possible_action

            goal_achieved = self.problem_state.goal_reached()

            if goal_achieved:
                break

        goal_achieved = self.problem_state.goal_reached()
        chat_history_content = self.get_chat_content_from_chat_history(chat_history)
        actions = {f"{i}": action for i, action in enumerate(actions)}

        return goal_achieved, chat_history_content, actions


if __name__ == "__main__":
    pass
