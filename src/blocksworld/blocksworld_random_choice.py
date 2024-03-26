import random
from typing import *
from langchain.chat_models.base import BaseChatModel

from blocksworld_validation_iterative_action import BlocksworldChat


class BlocksworldRandomChoice(BlocksworldChat):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

    def start_inference(
        self, with_current_state_prompt: bool = False, pbar=None
    ) -> Tuple[bool, str, Dict[str, Tuple[str, bool]]]:

        actions = []

        for i in range(self.config["max_iterations"]):
            possible_actions = self.problem_state.get_all_possible_actions()
            action = random.choice(possible_actions)
            action_text = self.action_to_text(action)
            actions.append(action_text)
            actions_return, is_action = self.take_action_from_text(action_text)

            if self.problem_state.goal_reached():
                break

        actions = {f"{i}": (action, True) for i, action in enumerate(actions)}
        chat_text = "Random Choice\n"
        goal_reached = self.problem_state.goal_reached()

        return goal_reached, chat_text, actions
