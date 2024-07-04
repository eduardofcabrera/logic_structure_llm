from typing import *

from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models.base import BaseChatModel

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.output_parsers import StrOutputParser

from src.blocksworld.blocksworld import Blocksworld
from langchain_core.runnables import Runnable

class BlocksworldChatWithPossibleActions(Blocksworld):
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
            
            prompt = (
                "[STATEMENT]\n"
                + current_state
                + goal
                + "\n[NEXT ACTION]\n"
                + possible_actions_text
                + order_prompt
            )
        
        return prompt
    
    def model_return_parser(self, model_return: str) -> str:
        model_return = model_return.lower()

        model_return = model_return.replace("reurn", "return")
        index = model_return.find("return")
        if index == -1:
            option_int = -1
        else:
            index = index + len("return") + 2
            try:
                option_str = model_return[index]
                option_int = int(option_str) - 1
            except:
                option_int = -1
        return option_int
    
    def take_action(self, option_int: int, possible_actions: List, possible_actions_text: List):
        
        if option_int == -1 or option_int >= len(possible_actions):
            return "no action", False
        
        action = possible_actions[option_int]
        self.problem_state.take_action(*action)
        action_text = possible_actions_text[option_int]
        
        return action_text, True

    def update_pbar(self, pbar, i):
        if pbar:
            pbar.set_description(
                f"Iteration: {i+1}/{self.config['max_iterations']}"
            )
            
    def logic_state_transition(self, possible_actions, possible_actions_text, states, actions):
        return possible_actions, possible_actions_text # This is a dummy function that does nothing       
    
    def update_chat_history(self, chat_history: List, prompt: str, action_int: str) -> List:
        chat_history.append(HumanMessage(content=prompt))
        chat_history.append(AIMessage(content="RETURN: " + str(action_int + 1)))
        return chat_history 
            
    def state_transition(self, chat_history: List, actions: List, states: List, chain: Runnable):
        
        current_state, possible_actions, possible_actions_text, goal = self.get_state()
        
        possible_actions, possible_actions_text = self.logic_state_transition(possible_actions, possible_actions_text, states, actions)
        
        prompt = self.get_prompt(chat_history, actions, states, current_state, goal, possible_actions, possible_actions_text)
        
        if len(possible_actions) == 1:
            model_return = "RETURN: 1"
        else:
            model_return = chain.invoke({"input": prompt, "chat_history": chat_history})
        returned_action = self.model_return_parser(model_return)
        action_text, is_action = self.take_action(returned_action, possible_actions, possible_actions_text)
        action_taken = (action_text, is_action)
        
        chat_history = self.update_chat_history(chat_history, prompt, returned_action)
        
        return chat_history, action_taken 
    
    def start_inference(self, pbar=None):
        
        chat_history = []
        actions = []
        states = [self.current_state_to_text()]
        chain = self.get_chain()
        
        for i in range(self.config["max_iterations"]):
            self.update_pbar(pbar, i)
            
            chat_history, action_taken = self.state_transition(chat_history, actions, states, chain)
            states.append(self.current_state_to_text())
            if not action_taken[1]:
                break
            
            actions.append(action_taken[0])
            
            if self.problem_state.goal_reached():
                break
            
                
        goal_achieved = self.problem_state.goal_reached() 
        chat_history_content = self.get_chat_content_from_chat_history(chat_history)
        actions = {f"{i}": (action, True) for i, action in enumerate(actions)}
        
        return goal_achieved, chat_history_content, actions

if __name__ == "__main__":
    pass