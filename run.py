import yaml
import random

import pandas as pd

from tqdm import tqdm
from datetime import datetime
from pathlib import Path

from parse_args import parse_args

from src import blocksworld_import
from src.blocksworld_import import Blocksworld

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama

def get_num_predict(task_config: str):
    if task_config == "configs/blocksworld_only_prompt.yaml" or task_config == "configs/blocksworld_only_prompt_iterative.yaml":
        return 128
    return 50

def get_model(model: str, temperature = 1, num_predict = 128):

    if "gpt" in model:
        return ChatOpenAI(model=model, temperature=temperature)
    elif "llama" in model:
        return ChatOllama(model=model, temperature=temperature, num_predict=num_predict)
    elif "mistral" in model or "mixtral" in model:
        return ChatOllama(model=model, temperature=temperature, num_predict=num_predict)
    else:
        raise Exception("Error model name")

def run_instance(config_run: dict, pbar=None):

    task_config_file = config_run["task_config"]

    with open(task_config_file) as f:
        task_config = yaml.safe_load(f)
        f.close()

    task_config.update(config_run)

    num_predict = get_num_predict(task_config["task_config"])
    model = get_model(model=config_run["model"], temperature=config_run["temperature"], num_predict=num_predict)

    Engine: Blocksworld = getattr(blocksworld_import, task_config["engine"])
    engine = Engine(config=task_config, model=model)

    result = engine.start_inference(pbar=pbar)

    return result

def json_to_df(dict) -> pd.DataFrame:

    instance_id_list = []
    goal_achieved_list = []
    content_list = []
    actions_text_list = []
    actions_possible_list = []
    n_actions_list = []
    for instance_id, value in dict.items():
        goal_achieved = value["goal_achieved"]
        content = value["content"]
        actions = value["actions"]
        actions_text = [action[0] for _, action in actions.items()]
        n_actions = len(actions_text)
        actions_possible = [str(int(action[1])) for _, action in actions.items()]
        actions_text = ".".join(actions_text)
        actions_possible = ".".join(actions_possible)

        instance_id_list.append(instance_id)
        goal_achieved_list.append(goal_achieved)
        content_list.append(content)
        actions_text_list.append(actions_text)
        actions_possible_list.append(actions_possible)
        n_actions_list.append(n_actions)

    df = pd.DataFrame(
        {
            "instance_id": instance_id_list,
            "goal_achieved": goal_achieved_list,
            "content": content_list,
            "actions_text": actions_text_list,
            "actions_possible": actions_possible_list,
            "n_actions": n_actions_list,
        }
    )

    return df

def n_actions(action_text: str) -> int:
    return len(action_text.split("."))

def ground_truth_n_actions(ground_truth_plan: str) -> int:
    return len(ground_truth_plan.split("\n")) - 1

def actions_possible(actions_dict: dict) -> str:
    return ".".join([str(int(action[1])) for _, action in actions_dict.items()])

def actions_text(actions_dict: dict) -> str:
    return ".".join([action[0] for _, action in actions_dict.items()])

def run_dataset(config_run: dict):
    dataset_folder = Path(config_run["dataset_folder"])
    if config_run["run_single"]:
        instance = dataset_folder / f"instance_{config_run['instance_id']}"
        instances = [instance]
    else:
        instances = list(dataset_folder.glob("*"))
        
        instances = random.sample(instances, int(len(instances)*config_run["sample_rate"]))
    
    pbar = tqdm(total=len(instances))
    returns = []
    for instance in instances:
        few_shot = instance / "few_shot.txt"
        ground_truth_plan = instance / "ground_truth_plan.txt"
        ground_truth_plan = open(ground_truth_plan, "r").read()
        pddl_file = instance / "pddl.pddl"
        config_run["few_shot"] = few_shot
        config_run["ground_truth_plan"] = ground_truth_plan
        config_run["pddl_file"] = pddl_file
        
        instance_return = [int(instance.stem[9:]), ground_truth_plan]
        instance_return += list(run_instance(config_run, pbar))
        
        returns.append(instance_return)
        
        pbar.update()
    
    df = pd.DataFrame(returns, columns=["instance_id", "ground_truth_plan", "goal_achieved", "content", "actions_text"])
    df["actions_possible"] = df["actions_text"].apply(actions_possible)
    df["actions_text"] = df["actions_text"].apply(actions_text)
    df["n_actions"] = df["actions_text"].apply(n_actions)
    df["ground_truth_n_actions"] = df["ground_truth_plan"].apply(ground_truth_n_actions)
    
    model_name = config_run["model"]
    today_date = datetime.today().strftime("%Y-%m-%d")
    today_date_ = datetime.today().strftime("%d_%H_%M")
    output_dir = Path(f"{config_run['json_output_dir']}/{today_date}")
    output_dir.mkdir(exist_ok=True)
    engine_type = (
        config_run["task_config"]
        .replace("configs/blocksworld_", "")
        .replace(".yaml", "")
    )
    if config_run["one_shot"]:
        model_name += "_one_shot"
    output_file = (
        output_dir
        / f"{today_date_}_{engine_type}_{dataset_folder.stem}_{config_run['sample_rate']}_T_{config_run['temperature']}_{model_name}.csv"
    )
    df.to_csv(output_file, index=False)
    

def main(config_run: dict):
    
    instance_range = config_run["instance_range"]

    instance_range = config_run["instance_range"]

    if config_run["run_single"]:
        inference_return = run_instance(config_run)
        print(*inference_return, sep="\n")
    else:
        returns = []

        pbar = tqdm(total=len(range(instance_range[0], instance_range[-1])))
        for instance_id in range(instance_range[0], instance_range[-1]):
            config_run["instance_id"] = instance_id
            returns.append(run_instance(config_run, pbar))
            pbar.update()

        json_out = {
            i: {
                "goal_achieved": _return[0],
                "content": _return[1],
                "actions": _return[2],
            }
            for i, _return in enumerate(returns)
        }
        
        df = json_to_df(json_out)

        model_name = config_run["model"]
        today_date = datetime.today().strftime("%Y-%m-%d")
        today_date_ = datetime.today().strftime("%d_%H_%M")
        output_dir = Path(f"{config_run['json_output_dir']}/{today_date}")
        output_dir.mkdir(exist_ok=True)
        engine_type = (
            config_run["task_config"]
            .replace("configs/blocksworld_", "")
            .replace(".yaml", "")
        )
        if config_run["one_shot"]:
            model_name += "_one_shot"
        output_file = (
            output_dir
            / f"{today_date_}_{engine_type}_{config_run['blocksworld']}_{instance_range[0]}_{instance_range[1]}_T_{config_run['temperature']}_{model_name}.csv"
        )
        df.to_csv(output_file, index=False)

if __name__ == "__main__":
    args = parse_args()
    config_file = args.config
    

    with open(config_file) as f:
        config_run = yaml.safe_load(f)
        f.close()

    random.seed(config_run["seed"])
    run_dataset(config_run)
    #main(config_run)
