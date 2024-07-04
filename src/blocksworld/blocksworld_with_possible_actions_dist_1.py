from typing import *

from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models.base import BaseChatModel
import random
from langchain_core.runnables import Runnable

from src.blocksworld.blocksworld_with_possible_actions import BlocksworldChatWithPossibleActions

import copy


class BlocksworldChatWithPossibleActionsDist1(BlocksworldChatWithPossibleActions):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)
    
    def logic_state_transition(self, possible_actions, possible_actions_text, states, actions):
        
        possible_actions_new = []
        possible_actions_text_new = []
        for i, (action, action_text) in enumerate(zip(possible_actions, possible_actions_text)):
            blocksworld_copy = copy.deepcopy(self)
            blocksworld_copy.problem_state.take_action(*action)
            possible_paths = blocksworld_copy.problem_state.get_all_possible_actions()
            if blocksworld_copy.problem_state.goal_reached() == True:
                return [action], [action_text]  
            if len(possible_paths) > 1: 
                possible_actions_new.append(action)
                possible_actions_text_new.append(action_text)  
        
        if len(states) >= 4 and len(possible_actions_new) > 1:
            if (states[-1] == states[-3]) and (states[-2] == states[-4]):
                remove_action = actions[-2]
                possible_actions_new = [action for action in possible_actions_new if self.action_to_text(action) != remove_action] 
                possible_actions_text_new = [action for action in possible_actions_text_new if action != remove_action] 
        
        possible_actions = possible_actions_new
        possible_actions_text = possible_actions_text_new
        
        return possible_actions, possible_actions_text
    
class BlocksworldChatWithPossibleActionsDist1Random(BlocksworldChatWithPossibleActionsDist1):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)
        
    def state_transition(self, chat_history: List, actions: List, states: List, chain: Runnable):
        
        current_state, possible_actions, possible_actions_text, goal = self.get_state()
        
        possible_actions, possible_actions_text = self.logic_state_transition(possible_actions, possible_actions_text, states, actions)
        
        prompt = self.get_prompt(chat_history, actions, states, current_state, goal, possible_actions, possible_actions_text)
        
        if len(possible_actions) == 1:
            model_return = "RETURN: 1"
        else:
            action_id = random.choice(range(len(possible_actions)))
            model_return = f"RETURN: {action_id + 1}"
        returned_action = self.model_return_parser(model_return)
        action_text, is_action = self.take_action(returned_action, possible_actions, possible_actions_text)
        action_taken = (action_text, is_action)
        
        chat_history = self.update_chat_history(chat_history, prompt, returned_action)
        
        return chat_history, action_taken 

if __name__ == "__main__":
    pass