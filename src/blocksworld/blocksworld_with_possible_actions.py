from typing import *

from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models.base import BaseChatModel

from blocksworld_validation_iterative_action import BlocksworldChat


class BlocksworldChatWithPossibleActions(BlocksworldChat):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

    def get_first_prompt(self) -> str:

        current_condition_text = self.current_state_to_text()
        goal_text = self.goal_to_text()
        possible_actions_text = self.possible_actions_to_text()
        few_shot_text = self.get_one_shot_text()
        order_prompt = self.config["prompts"]["order_prompts"]

        order_prompt = """\n Answer based on the example above.\n\nReturn the number of the best next action to achieve my goal. Write only with:\n```RETURN: <OPTION NUMBER>.```"""

        first_prompt = (
            self.config["domain_intro"]
            + few_shot_text
            + "\n[STATEMENT]\n"
            + current_condition_text
            + goal_text
            + "\n[NEXT ACTION]\n"
            + possible_actions_text
            + order_prompt
        )

        return first_prompt

    def get_prompt(self) -> str:
        current_condition_text = self.current_state_to_text()
        goal_text = self.goal_to_text()
        possible_actions_text = self.possible_actions_to_text()
        order_prompt = self.config["prompts"]["order_prompts"]

        actions_taken = self.problem_state.actions_taken
        actions_taken_text = "\nSequence of actions already taken to achieve my goal:\n"
        for action in actions_taken:
            action_text = self.action_to_text(action)
            actions_taken_text += action_text + "\n"

        order_prompt = """\nReturn the number of the best next action to achieve my goal. Write only with:\n```RETURN: <OPTION NUMBER>.```"""

        prompt = (
            "[STATEMENT]\n"
            + current_condition_text
            + goal_text
            + "\n[NEXT ACTION]\n"
            + possible_actions_text
            + order_prompt
        )

        return prompt

    def start_inference(self, pbar=None) -> Tuple[bool, str, List[str]]:

        chain = self.get_chain()

        chat_history = []
        actions = []

        first_prompt = self.get_first_prompt()
        model_return, chat_history = self.chat_iteration(
            first_prompt, chat_history, chain
        )

        prompt = ""
        for i in range(self.config["max_iterations"]):
            if pbar:
                pbar.set_description(f"Iteration: {i}/{self.config['max_iterations']}")

            model_return = model_return.lower()

            model_return = model_return.replace("reurn", "return")
            index = model_return.find("return")
            if index == -1:
                print(model_return)
                break
            else:
                index = index + len("return") + 2
                try:
                    option_str = model_return[index]
                    option_int = int(option_str) - 1
                except:
                    print(model_return)
                    break

            possible_actions = self.problem_state.get_all_possible_actions()
            if option_int >= len(possible_actions):
                print(model_return)
                break
            action = possible_actions[option_int]
            self.problem_state.take_action(*action)
            actions.append(self.action_to_text(action))

            if self.problem_state.goal_reached():
                break

            chat_history[-1].content = "RETURN: " + option_str
            prompt = self.get_prompt()
            model_return, chat_history = self.chat_iteration(
                prompt, chat_history, chain
            )

        goal_reached = self.problem_state.goal_reached()
        self.reboot_problem_state()

        chat_history.append(HumanMessage(content=prompt))
        chat_history.append(AIMessage(content=model_return))

        actions = {f"{i}": (action, True) for i, action in enumerate(actions)}
        chat_history_text = self.get_chat_content_from_chat_history(chat_history)

        return goal_reached, chat_history_text, actions
