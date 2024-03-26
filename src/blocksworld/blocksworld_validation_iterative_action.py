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

from blocksworld import Blocksworld


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
        few_shot_text = self.get_one_shot_text()

        first_prompt = (
            self.config["domain_intro"]
            + few_shot_text
            + "\n[STATEMENT]\n"
            + current_condition_text
            + goal_text
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

    def start_inference(
        self, with_current_state_prompt: bool = False, pbar=None
    ) -> Tuple[bool, str, Dict[str, Tuple[str, bool]]]:

        chat_chain = self.get_chain()

        chat_history = []
        actions = []

        first_prompt_text = self.get_first_prompt()
        model_return, chat_history = self.chat_iteration(
            first_prompt_text, chat_history, chat_chain
        )

        for i in range(self.config["max_iterations"]):

            if pbar:
                pbar.set_description(f"Iteration: {i}/{self.config['max_iterations']}")

            index = model_return.find("THE NEXT BEST ACTION IS: ")
            if index == -1:
                action = "no action"
            else:
                try:
                    action = self.filter_text_action(model_return)
                except:
                    action = "no action"

            action_return, is_action = self.take_action_from_text(action)
            actions.append((action, action_return))

            if not (is_action):
                break

            if self.problem_state.goal_reached():
                break

            chat_history[-1].content = "THE NEXT BEST ACTION IS: " + action
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
