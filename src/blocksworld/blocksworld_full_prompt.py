from typing import *

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models.base import BaseChatModel
from langchain_core.runnables import Runnable

from src.blocksworld.blocksworld import Blocksworld

from src.blocksworld.utils import is_valid_action


class BlocksworldOnlyPrompt(Blocksworld):
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

        chain = prompt | model | str_output_parser

        return chain

    def get_few_shot_text(self) -> str:
        file = open(self.config["few_shot"], "r")
        few_shot = file.read()

        return few_shot

    def get_prompt(
        self, chat_history: List, actions: List, current_state: str, goal: str
    ) -> str:

        domain_intro = self.config["domain_intro"]
        few_shot_text = self.get_few_shot_text()
        cot_prompt = "\n\n[STATEMENT]\nAs initial conditions I have that, the red block is clear, the blue block is clear, the yellow block is clear, the hand is empty, the blue block is on top of the orange block, the red block is on the table, the orange block is on the table and the yellow block is on the table\nMy goal is to have that the orange block is on top of the blue block.\nMy plan is as follows:\n\n[PLAN]\n1. Current State: the red block is clear, the blue block is clear, the yellow block is clear, the hand is empty, the blue block is on top of the orange block, the red block is on the table, the orange block is on the table and the yellow block is on the table\n   Action: unstack the blue block from on top of the orange block\n   Reason: The above action is applicable in the current state because its preconditions; the blue block is clear, the hand is empty and the blue block is on top of the orange block, are satisfied in the current state.\n   Resulting State: the red block is clear, the orange block is clear, the yellow block is clear, the hand is currently holding blue block, the red block is on the table, the orange block is on the table and the yellow block is on the table\n\n2. Current State: the red block is clear, the orange block is clear, the yellow block is clear, the hand is currently holding blue block, the red block is on the table, the orange block is on the table and the yellow block is on the table\n   Action: put down the blue block\n   Reason: The above action is applicable in the current state because its preconditions; the hand is currently holding blue block, are satisfied in the current state.\n   Resulting State: the red block is clear, the blue block is clear, the orange block is clear, the yellow block is clear, the hand is empty, the red block is on the table, the blue block is on the table, the orange block is on the table and the yellow block is on the table\n\n3. Current State: the red block is clear, the blue block is clear, the orange block is clear, the yellow block is clear, the hand is empty, the red block is on the table, the blue block is on the table, the orange block is on the table and the yellow block is on the table\n   Action: pick up the orange block\n   Reason: The above action is applicable in the current state because its preconditions; the orange block is clear, the hand is empty and the orange block is on the table, are satisfied in the current state.\n   Resulting State: the red block is clear, the blue block is clear, the yellow block is clear, the hand is currently holding orange block, the red block is on the table, the blue block is on the table and the yellow block is on the table\n\n4. Current State: the red block is clear, the blue block is clear, the yellow block is clear, the hand is currently holding orange block, the red block is on the table, the blue block is on the table and the yellow block is on the table\n   Action: stack the orange block on top of the blue block\n   Reason: The above action is applicable in the current state because its preconditions; the blue block is clear and the hand is currently holding orange block, are satisfied in the current state.\n   Resulting State: the red block is clear, the orange block is clear, the yellow block is clear, the hand is empty, the orange block is on top of the blue block, the red block is on the table, the blue block is on the table and the yellow block is on the table\n\nFinal State: the red block is clear, the orange block is clear, the yellow block is clear, the hand is empty, the orange block is on top of the blue block, the red block is on the table, the blue block is on the table and the yellow block is on the table\nThe goal conditions are satisfied in the final state. Hence, the above plan is valid.\n[PLAN END]\n\n"
        # order_prompt = """\nReturn only the sequence of actions as the example above, nothing more.\nReturn the plan that makes me achieve my goal.\nWrite only:\n ```<plan>\n[PLAN]\n<\plan>```"""
        order_prompt = "\nMy plan is as follows:\n"
        prompt = (
            domain_intro
            # + few_shot_text
            + cot_prompt
            + "\n[STATEMENT]\n"
            + current_state
            + goal
            + order_prompt
        )
        return prompt

    def model_return_parser(self, model_return: str) -> List[str]:
        actions = model_return.split("\n")
        actions = [self.filter_text_action(action) for action in actions]

        return [action for action in actions if is_valid_action(action, self.config)]

        new_actions = []
        found_valid = False
        for action in actions:
            action_valid = is_valid_action(action, self.config)
            if found_valid and not (action_valid):
                break
            if action_valid:
                new_actions.append(action)
                found_valid = True

        return new_actions

    def take_actions(self, actions: List[str]) -> Dict[str, Tuple[str, bool]]:
        actions = {
            f"{i}": (action, self.take_action_from_text(action))
            for i, action in enumerate(actions)
        }

        actions = {
            key: (value[0], value[1][0])
            for key, value in actions.items()
            if value[1][1]
        }

        return actions

    def update_chat_history(
        self, chat_history: List, prompt: str, model_return: str
    ) -> List:
        chat_history.append(HumanMessage(content=prompt))
        chat_history.append(AIMessage(content=model_return))

        return chat_history

    def state_transition(self, chat_history: List, actions: List, chain: Runnable):

        current_state, _, _, goal = self.get_state()
        prompt = self.get_prompt(chat_history, actions, current_state, goal)

        model_return = chain.invoke({"input": prompt, "chat_history": chat_history})
        returned_actions = self.model_return_parser(model_return)
        actions_taken = self.take_actions(returned_actions)

        model_return = "<plan>\n" + "\n".join(returned_actions) + "\n<\plan>"
        chat_history = self.update_chat_history(chat_history, prompt, model_return)

        return chat_history, actions_taken

    def start_inference(self, pbar=None):

        chat_history = []
        actions = []
        chain = self.get_chain()

        chat_history, actions = self.state_transition(chat_history, actions, chain)

        goal_achieved = self.problem_state.goal_reached()
        chat_history_content = self.get_chat_content_from_chat_history(chat_history)

        return goal_achieved, chat_history_content, actions


if __name__ == "__main__":
    pass
