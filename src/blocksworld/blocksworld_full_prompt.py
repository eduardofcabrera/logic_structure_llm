from typing import *

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models.base import BaseChatModel
from langchain_core.runnables import Runnable

from blocksworld import Blocksworld


class BlocksworldOnlyPrompt(Blocksworld):
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

    def start_inference(
        self, pbar: None
    ) -> Tuple[bool, str, Dict[str, Tuple[str, bool]]]:

        chain = self.get_chain()

        _input = self.instance_prompt["query"]
        input_split = "My plan is as follows:".join(
            _input.split("My plan is as follows:")[:-1]
        )
        order_prompt = """\nReturn only the sequence of actions as the example above, nothing more.\nReturn the plan that makes me achieve my goal.\n Write only:\n ```<plan>\n[PLAN]\n<\plan>```"""

        _input = input_split + order_prompt
        chat_history = []

        model_return = chain.invoke({"input": _input, "chat_history": chat_history})
        chat_history.append(HumanMessage(content=_input))
        chat_history.append(AIMessage(content=model_return))

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
        chat_history_content = self.get_chat_content_from_chat_history(chat_history)

        self.reboot_problem_state()

        return goal_reached, chat_history_content, actions
