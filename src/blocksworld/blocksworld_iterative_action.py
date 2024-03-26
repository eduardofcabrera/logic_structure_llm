from typing import *

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models.base import BaseChatModel
from langchain_core.runnables import Runnable

from blocksworld_validation_iterative_action import BlocksworldChat


class BlocksworldIterativeActions(BlocksworldChat):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

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
            + self.config["prompts"]["order_prompts"]
        )

        return first_prompt

    def get_action_return_prompt(
        self, action_return: bool, with_current_state_prompt: bool = False
    ) -> str:

        state_text = self.current_state_to_text() if with_current_state_prompt else ""

        feedback_prompt = ""
        order_prompt = self.config["prompts"]["order_prompts"]

        return feedback_prompt + state_text + order_prompt

    def get_check_goal_chain(self) -> Runnable:
        model = self.model
        str_output_parser = StrOutputParser()
        prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "user",
                    "Check if the goal is reached. Return only with: ```RETURN: <YES/NO>```",
                ),
            ]
        )

        chat_chain = prompt | model | str_output_parser
        return chat_chain

    def start_inference(
        self, with_current_state_prompt: bool = False, pbar=None
    ) -> Tuple[bool, str, Dict[str, Tuple[str, bool]]]:

        chat_chain = self.get_chain()
        check_goal_chain = self.get_check_goal_chain()

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
            chat_history[-1].content = "THE NEXT BEST ACTION IS: " + action

            if not (is_action):
                break

            model_return_check_goal = check_goal_chain.invoke(
                {"chat_history": chat_history}
            )
            model_return_check_goal = model_return_check_goal.lower()
            model_return_check_goal = model_return_check_goal.replace("reurn", "return")

            index = model_return_check_goal.find("return")
            if index == -1:
                goal_reached = False
            else:
                index = index + len("return") + 2
                try:
                    goal_reached = model_return_check_goal[index] == "y"
                except:
                    goal_reached = False

            if goal_reached:
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
