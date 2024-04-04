from typing import *

from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models.base import BaseChatModel

from src.blocksworld.blocksworld_validation_iterative_action import BlocksworldChat

import copy


class BlocksworldChatWithPossibleActionsLoop(BlocksworldChat):
    def __init__(self, config: Dict, model: BaseChatModel):
        super().__init__(config=config, model=model)

    @property
    def num_predict(self):
        return 50
    
    def get_first_prompt(self) -> str:

        current_condition_text = self.current_state_to_text()
        goal_text = self.goal_to_text()
        possible_actions_text, removed_action = self.possible_actions_to_text()
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

        return first_prompt, removed_action

    def possible_actions_to_text(self, actions = None, states = None) -> str:
        possible_actions = self.problem_state.get_all_possible_actions()
        actions_texts = [self.action_to_text(action) for action in possible_actions]
        actions_texts.sort()
        removed_action = None
        removed_possible_actions = self.get_possible_paths()
        removed_possible_actions_text = [self.action_to_text(action) for action in removed_possible_actions]
        
        
        actions_texts = [action_text for action_text in actions_texts if action_text not in removed_possible_actions_text]
        
        if actions and states:
            len_states = len(states)
            if len_states > 2 and len(actions_texts) > 1:
                state_prev = states[-3]
                if state_prev == states[-1]:
                    action = actions[-2]
                    actions_texts = [action_text for action_text in actions_texts if action_text != action]
                    removed_action = action

        possible_actions_text = "Possible actions:\n"
        for i, action_text in enumerate(actions_texts):
            possible_actions_text += f"{i+1}: {action_text}\n"
            
        if removed_action:
            removed_possible_actions_text.append(removed_action)
        

        return possible_actions_text, removed_possible_actions_text
    
    def get_prompt(self, actions, states) -> str:
        current_condition_text = self.current_state_to_text()
        goal_text = self.goal_to_text()
        possible_actions_text, removed_action = self.possible_actions_to_text(actions, states)
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

        return prompt, removed_action
    
    def get_possible_paths(self):
        
        possible_actions = self.problem_state.get_all_possible_actions()
        possible_paths_dict = {}
        for i, action in enumerate(possible_actions):
            blocksworld_copy = copy.deepcopy(self)
            blocksworld_copy.problem_state.take_action(*action)
            possible_paths = blocksworld_copy.problem_state.get_all_possible_actions()
            if len(possible_paths) <= 1 and blocksworld_copy.problem_state.goal_reached() == False: 
                possible_paths_dict[i] = (action, len(possible_paths))

        return [action for i, (action, _) in possible_paths_dict.items()]
        

    
    def start_inference(self, pbar=None) -> Tuple[bool, str, List[str]]:

        chain = self.get_chain()

        chat_history = []
        actions = []
        states = [self.current_state_to_text()]

        first_prompt, removed_action = self.get_first_prompt()
        check_actions = (first_prompt.split("Possible actions:\n")[-1].split("Answer based on the example")[0]).split("\n")[:-2]
        if len(check_actions) == 1:
            model_return = "RETURN: 1"
            chat_history.append(HumanMessage(content=first_prompt))
            chat_history.append(AIMessage(content=model_return))
        else:
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
            possible_actions_dict = {
                self.action_to_text(possible_action): possible_action
                for possible_action in possible_actions
            }
            possible_actions = list(dict(sorted(possible_actions_dict.items())).values())
            if removed_action:
                possible_actions = [action for action in possible_actions if self.action_to_text(action) not in removed_action]
            if option_int >= len(possible_actions):
                print(model_return)
                break
            action = possible_actions[option_int]
            self.problem_state.take_action(*action)
            actions.append(self.action_to_text(action))

            if self.problem_state.goal_reached():
                break

            chat_history[-1].content = "RETURN: " + option_str
            prompt, removed_action = self.get_prompt(actions, states)
            check_actions = (prompt.split("Possible actions:\n")[-1].split("Return the number of the best")[0]).split("\n")[:-2]
            if len(check_actions) == 1:
                model_return = "RETURN: 1"
                chat_history.append(HumanMessage(content=prompt))
                chat_history.append(AIMessage(content=model_return))
            else:
                model_return, chat_history = self.chat_iteration(
                    prompt, chat_history, chain
                )
            states.append(self.current_state_to_text())

        goal_reached = self.problem_state.goal_reached()
        self.reboot_problem_state()

        chat_history.append(HumanMessage(content=prompt))
        chat_history.append(AIMessage(content=model_return))

        actions = {f"{i}": (action, True) for i, action in enumerate(actions)}
        chat_history_text = self.get_chat_content_from_chat_history(chat_history)

        return goal_reached, chat_history_text, actions

if __name__ == "__main__":
    pass