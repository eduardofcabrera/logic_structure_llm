import argparse
import yaml
import json

from tqdm import tqdm

import blocksworld
from blocksworld import Blocksworld

from langchain_openai import ChatOpenAI


def run_instance(config_run: dict):

    task_config_file = config_run["task_config"]

    with open(task_config_file) as f:
        task_config = yaml.safe_load(f)
        f.close()

    task_config.update(config_run)

    model = ChatOpenAI(model=config_run["model"])

    Engine: Blocksworld = getattr(blocksworld, task_config["engine"])

    engine = Engine(config=task_config, model=model)

    result = engine.start_inference()

    return result


def main(config_run: dict):

    if config_run["run_single"]:
        inference_return = run_instance(config_run)
        print(*inference_return, sep="\n")
    else:
        returns = []

        for instance_id in tqdm(range(12, 27)):
            config_run["instance_id"] = instance_id
            returns.append(run_instance(config_run))

        json_out = {
            i: {
                "chat_with_possible_actions": {
                    "goal_achieved": _return[0],
                    "content": _return[1],
                    "actions": _return[2],
                },
            }
            for i, _return in enumerate(returns)
        }

        with open(config_run["json_output"], "w") as f:
            json.dump(json_out, f)


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

    main(config_run)