import re
from typing import *


def is_valid_action(action_text: str, config: Dict):
    actions_text_mapping = config["actions"]

    actions_text_match = {
        action_name: re.match(action_text_format.replace("{}", "(.*)"), action_text)
        for action_name, action_text_format in actions_text_mapping.items()
    }

    action_match = [
        action_name
        for action_name, action_text_match in actions_text_match.items()
        if action_text_match
    ]

    if len(action_match) != 1:
        return False
    return True

if __name__ == "__main__":
    pass
