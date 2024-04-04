from typing import *

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import HumanMessage, AIMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models.base import BaseChatModel
from langchain_core.runnables import Runnable

from src.blocksworld.blocksworld import Blocksworld


class BlocksworldOnlyPromptIterative(Blocksworld):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

    def get_chain(self) -> Runnable:
        model = self.model
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
    
    def get_first_prompt(self) -> str:
        
        domain_intro = self.config["domain_intro"]
        few_shot_text = self.get_few_shot_text()
        current_condition_text = self.current_state_to_text()
        goal_text = self.goal_to_text()
        order_prompt = """\nReturn only the sequence of actions as the example above, nothing more.\nReturn the plan that makes me achieve my goal.\n Write only:\n ```<plan>\n[PLAN]\n<\plan>```"""
        
        first_prompt = (
            domain_intro
            + few_shot_text
            + "\n[STATEMENT]\n"
            + current_condition_text
            + goal_text
            + order_prompt
        )
        
        return first_prompt

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
        self, pbar=None
    ) -> Tuple[bool, str, Dict[str, Tuple[str, bool]]]:

        chain = self.get_chain()
        chat_history = []

        _input = self.get_first_prompt()

        model_return, chat_history = self.chat_iteration(_input, chat_history, chain)
        model_return_list = [model_return]

        for i in range(self.config["max_iterations_prompt_iterative"]):
            if pbar:
                pbar.set_description(
                    f"Iteration: {i}/{self.config['max_iterations_prompt_iterative']}"
                )

            actions = model_return.split("\n")
            actions = [self.filter_text_action(action) for action in actions]
            actions = {
                f"{i}": (action, self.take_action_from_text(action))
                for i, action in enumerate(actions)
            }

            actions = {
                key: (value[0], value[1][0])
                for key, value in actions.items()
                if value[1][1]
            }

            goal_reached = self.problem_state.goal_reached()
            correct_response = goal_reached
            not_possible_actions = [
                value[1] for key, value in actions.items() if not value[1]
            ]
            if len(not_possible_actions) != 0:
                correct_response = False
            if correct_response:
                break

            prompt = "The previous plan was incorrect please correct it and write it again. Return the plan that makes me achieve my goal.\n Write only:\n ```<plan>\n[PLAN]\n<\plan>```\n"
            model_return, chat_history = self.chat_iteration(
                prompt, chat_history, chain
            )
            model_return_list.append(model_return)
            self.reboot_problem_state()

        chat_content = self.get_chat_content_from_chat_history(chat_history)
        self.reboot_problem_state()

        return goal_reached, chat_content, actions

if __name__ == "__main__":
    pass