import argparse
import yaml
import json

from tqdm import tqdm

from blocksworld import Blocksworld

from langchain_openai import ChatOpenAI


def main(config_run: dict):

    task_config_file = config_run["task_config"]

    with open(task_config_file) as f:
        task_config = yaml.safe_load(f)
        f.close()

    task_config.update(config_run)

    model = ChatOpenAI(model=config_run["model"])

    blocksworld_run = Blocksworld(config=task_config, model=model)

    returns_chat = blocksworld_run.start_chat()
    returns_only_prompt = blocksworld_run.start_chat_only_prompt()

    return (returns_only_prompt, returns_chat)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    config_file = args.config

    with open(config_file) as f:
        config_run = yaml.safe_load(f)
        f.close()

    returns = []

    for instance_id in tqdm(range(12, 23)):
        config_run["instance_id"] = instance_id
        returns.append(main(config_run))

    json_out = {
        i: {
            "only_prompt": {
                "goal_achieved": _return[0][0],
                "content": _return[0][1],
                "actions": _return[0][2],
            },
            "chat": {
                "goal_achieved": _return[1][0],
                "content": _return[1][1],
                "actions": _return[1][2],
            },
        }
        for i, _return in enumerate(returns)
    }

    with open("json_out_3_1.json", "w") as f:
        json.dump(json_out, f)
