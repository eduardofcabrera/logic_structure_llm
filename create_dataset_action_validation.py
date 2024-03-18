from typing import Dict
import yaml
import random
import pandas as pd
from tqdm import tqdm
from pathlib import Path

from parse_args import parse_args

from blocksworld import Blocksworld

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_model(model: str):
    
    if "gpt" in model:
        return ChatOpenAI(model=model)
    elif "llama" in model:
        return Ollama(model=model)
    elif "mistral" in model:
        return ChatOllama(model=model)
    else:
        raise Exception("Error model name")

def create_dataset(config_run: Dict):
    instance_id_min = config_run["instance_id_range"][0]
    instance_id_max = config_run["instance_id_range"][1]
    impossible_n_actions = config_run["impossible_n_actions"]
    
    task_config_file = config_run["task_config"]
    with open(task_config_file) as f:
        task_config = yaml.safe_load(f)
        f.close()
        
    task_config.update(config_run)
    
    model = get_model(model=config_run["model"])
    
    df = pd.DataFrame([])
    for instance_id in tqdm(range(instance_id_min, instance_id_max)):
        task_config["instance_id"] = instance_id
        blocksworld = Blocksworld(task_config, model)
        
        current_context_text = blocksworld.current_state_to_text()
        
        possible_actions = blocksworld.problem_state.get_all_possible_actions()
        impossible_actions = blocksworld.problem_state.get_all_impossible_actions()
        impossible_actions = random.sample(impossible_actions, impossible_n_actions)
        
        possible_options = [1]*len(possible_actions)
        impossible_options = [2]*len(impossible_actions)
        
        possible_actions.extend(impossible_actions)
        possible_options.extend(impossible_options)
        
        for action, option in zip(possible_actions, possible_options):
            action_text = blocksworld.action_to_text(action)
            df_ = pd.DataFrame({
                "instance_id": [instance_id],
                "action": [action_text],
                "current_state": [current_context_text],
                "action_possible": [option],
            })
            
            df = pd.concat([df, df_])
    
    dataset_output_file = task_config["dataset_output_file"]
    df.to_csv(f"{dataset_output_file}_{instance_id_min}_{instance_id_max}_{impossible_n_actions}.csv")


def inference(config_run: Dict):
    
    dataset_file = Path(config_run["dataset_file"])
    dataset = pd.read_csv(dataset_file)
    y_hat = []
    model_return_list = []
    
    task_config_file = config_run["task_config"]
    with open(task_config_file) as f:
        task_config = yaml.safe_load(f)
        f.close()
        
    task_config.update(config_run)
    
    model = get_model(model=config_run["model"])
    str_output_parser = StrOutputParser()
    
    prompt = PromptTemplate.from_template(
"""
{domain_intro}

[STATEMENT]
{current_context_text}                                        

action: {action_text}

Is the above action allowed taking into account the rules stated and the current state of the problem?

1. Action is allowed.
2. Action is not allowed.

Write only with:
    ```RETURN: <OPTION NUMBER>.```
""")
        
    chain = prompt | model | str_output_parser
    
    for row_id in tqdm(range(dataset.shape[0])):
        row = dataset.iloc[row_id]
        action_text = row["action"]
        current_context_text = row["current_state"]
        domain_intro = task_config["domain_intro"]
        
        model_return = chain.invoke({
                "domain_intro": domain_intro, "current_context_text": current_context_text, "action_text": action_text
            })
        
        model_return_list.append(model_return)
        
        model_return = model_return.lower()
        
        index = model_return.find("return")
        if index == -1:
            allowed = model_return.find(". action is allowed.")
            not_allowed = model_return.find(". action is not allowed")
            if allowed != -1:
                option_int = 1
            elif not_allowed != -1:
                option_int = 2
            else:
                option_int = -1
        else:
            index = index + len("return") + 2
            option_str = model_return[index]
            try:
                option_int = int(option_str)
                if not(option_int == 1 or option_int == 2):
                    option_int = -1
            except:
                option_int = -1
        
        y_hat.append(option_int)
        
    dataset["action_possible_inference"] = y_hat
    dataset["model_return"] = model_return_list
    
    model_name = task_config["model"]
    dataset.to_csv(f"experiments_results/{dataset_file.stem}_{model_name}.csv")

if __name__ == "__main__":
    
    args = parse_args()
    config_file = args.config
    
    with open(config_file) as f:
        config_run = yaml.safe_load(f)
        f.close()
    
    if config_run["create_dataset"]:
        create_dataset(config_run)
    else:
        inference(config_run)