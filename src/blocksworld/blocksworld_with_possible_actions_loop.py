from typing import *

from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models.base import BaseChatModel

from src.blocksworld.blocksworld_with_possible_actions import BlocksworldChatWithPossibleActions

import copy


class BlocksworldChatWithPossibleActionsLoop(BlocksworldChatWithPossibleActions):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)
    
    def logic_state_transition(self, possible_actions, possible_actions_text, states, actions):
        possible_actions = list(zip(possible_actions, possible_actions_text))
        if len(states) > 2 and len(possible_actions) > 1:
            state_prev = states[-3]
            if state_prev == states[-1]:
                action = actions[-2]
                possible_actions = [possible_action for possible_action in possible_actions if possible_action[1] != action]
        
        possible_actions = [possible_action[0] for possible_action in possible_actions] 
        possible_actions_text = [possible_action[1] for possible_action in possible_actions] 
        
        return possible_actions, possible_actions_text

if __name__ == "__main__":
    pass