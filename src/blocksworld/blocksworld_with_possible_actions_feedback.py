from typing import *

from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models.base import BaseChatModel

from src.blocksworld.blocksworld_with_possible_actions import BlocksworldChatWithPossibleActions


class BlocksworldChatWithPossibleActionsFeedback(BlocksworldChatWithPossibleActions):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

    def get_prompt(self, chat_history: List, actions: List, states: List, current_state: str, goal: str, possible_actions: List, possible_actions_text: List) -> str:
        
        possible_actions_text = self.possible_actions_to_text(possible_actions)
        order_prompt = """\n\nReturn the number of the best next action to achieve my goal. Write only with:\n```RETURN: <OPTION NUMBER>.```"""
        if len(chat_history) == 0:

            prompt = (
                self.config["domain_intro"]
                + "\n[STATEMENT]\n"
                + current_state
                + goal
                + "\n[NEXT ACTION]\n"
                + possible_actions_text
                + order_prompt
            )
        else:
            
            loop_str = ""
            if current_state in states[:-1]:
                loop_str = "\n\nYou have already been in this state. Try another sequence of actions.\n\n"
            
            prompt = (
                "[STATEMENT]\n"
                + current_state
                + goal
                + loop_str
                + "\n[NEXT ACTION]\n"
                + possible_actions_text
                + order_prompt
            )
        
        return prompt

if __name__ == "__main__":
    pass