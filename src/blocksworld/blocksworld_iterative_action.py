from typing import *

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage, AIMessage, BaseMessage
from langchain.chat_models.base import BaseChatModel
from langchain_core.runnables import Runnable

from src.blocksworld.blocksworld_validation_iterative_action import BlocksworldChat
from src.blocksworld.blocksworld import Blocksworld


class BlocksworldIterativeActions(Blocksworld):
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
    
    def get_check_goal_chain(self) -> Runnable:
        model = self.model()
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
    
    def get_prompt(self, chat_history: List, actions: List, current_state: str, goal: str) -> str:
        
        if len(chat_history) == 0:
            few_shot_text = self.get_one_shot_text()
            prompt = (
                self.config["domain_intro"]
                + few_shot_text
                + "\n[STATEMENT]\n"
                + current_state
                + goal
                + self.config["prompts"]["order_prompts"]
            )
        else:
            order_prompt = self.config["prompts"]["order_prompts"]
            prompt = order_prompt
        
        return prompt
    
    def model_return_parser(self, model_return: str) -> str:
        index = model_return.find("THE NEXT BEST ACTION IS: ")
        if index == -1:
            action = "no action"
        else:
            try:
                action = self.filter_text_action(model_return)
            except:
                action = "no action"
        return action
    
    def check_goal_model_return_parser(self, model_return: str) -> bool:
        model_return_check_goal = model_return.lower()
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
        
        return goal_reached
    
    def update_chat_history(self, chat_history: List, prompt: str, action: str) -> List:
        chat_history.append(HumanMessage(content=prompt))
        chat_history.append(AIMessage(content="THE NEXT BEST ACTION IS: " + action))
        return chat_history
       
    def state_transition(self, chat_history: List, actions: List, chain: Runnable):
        
        current_state, _, _, goal = self.get_state()
        prompt = self.get_prompt(chat_history, actions, current_state, goal)
        
        model_return = chain.invoke({"input": prompt, "chat_history": chat_history})
        returned_action = self.model_return_parser(model_return)
        is_possible_action, is_action = self.take_action_from_text(returned_action)
        action_taken = (returned_action, is_possible_action, is_action)
        
        chat_history = self.update_chat_history(chat_history, prompt, returned_action)
        
        return chat_history, action_taken     
    
    def update_pbar(self, pbar, i):
        if pbar:
            pbar.set_description(
                f"Iteration: {i+1}/{self.config['max_iterations']}"
            )
            
    def state_avaluation(self, chat_history: List, check_goal_chain: Runnable):
        
        model_return_check_goal = check_goal_chain.invoke(
            {"chat_history": chat_history}
        )
        goal_reached = self.check_goal_model_return_parser(model_return_check_goal)
        return goal_reached
        
    
    def start_inference(self, pbar=None):
        
        chat_history = []
        actions = []
        chain = self.get_chain()
        check_goal_chain = self.get_check_goal_chain()
        
        for i in range(self.config["max_iterations"]):
            self.update_pbar(pbar, i)
            
            chat_history, action_taken = self.state_transition(chat_history, actions, chain)
            if not action_taken[-1]: # is not an action
                break
            actions.append((action_taken[0], action_taken[1])) # action name and is_possible_action
            
            goal_achieved = self.state_avaluation(chat_history, check_goal_chain) 
            
            if goal_achieved:
                break
                
        goal_achieved = self.problem_state.goal_reached() 
        chat_history_content = self.get_chat_content_from_chat_history(chat_history)
        actions = {f"{i}": action for i, action in enumerate(actions)}
        
        return goal_achieved, chat_history_content, actions

if __name__ == "__main__":
    pass