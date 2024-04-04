from typing import Dict
import yaml
import random
import pandas as pd
from tqdm import tqdm
from pathlib import Path

from parse_args import parse_args

from _blocksworld import Blocksworld, is_valid_action

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
        goal_text = blocksworld.goal_to_text()
        possible_actions = blocksworld.problem_state.get_all_possible_actions()
        possible_actions = map(blocksworld.action_to_text, possible_actions)
        possible_actions = ".".join(possible_actions)
        
        df_ = pd.DataFrame({
            "instance_id": [instance_id],
            "current_state": [current_context_text],
            "goal_text": [goal_text],
            "possible_actions": [possible_actions],
            "rank": [0]
        })
        
        df = pd.concat([df, df_])
        
        action = possible_actions[0]
        blocksworld.take_action_from_text(action)
        
        current_context_text = blocksworld.current_state_to_text()
        goal_text = blocksworld.goal_to_text()
        possible_actions = blocksworld.problem_state.get_all_possible_actions()
        possible_actions = map(blocksworld.action_to_text, possible_actions)
        possible_actions = ".".join(possible_actions)
        
        df_ = pd.DataFrame({
            "instance_id": [instance_id],
            "current_state": [current_context_text],
            "goal_text": [goal_text],
            "possible_actions": [possible_actions],
            "rank": [1]
        })
                
        df = pd.concat([df, df_])
        
    dataset_output_file = task_config["output_file"]   
    df.to_csv(f"{dataset_output_file}_{instance_id_min}_{instance_id_max}.csv")  

def inference(config_run: Dict):
    task_config_file = config_run["task_config"]
    with open(task_config_file) as f:
        task_config = yaml.safe_load(f)
        f.close()
        
    task_config.update(config_run)
    
    dataset_file = Path(config_run["dataset_file"])
    dataset = pd.read_csv(dataset_file)
    
    model = get_model(model=config_run["model"])
    str_output_parser = StrOutputParser()
    prompt = PromptTemplate.from_template(
"""
{domain_intro}

[STATEMENT]
{current_context_text}                                        
{goal_text}

Return the next action to achieve my goal. Return one, and only one, action, without nothing more.
Write only with:
    ```THE NEXT BEST ACTION IS: <action>.```
""")
    
    chain = prompt | model | str_output_parser
    
    action_possible_list = []
    model_return_list = []
    action_list = []
    for row_id in tqdm(range(dataset.shape[0])):
        row = dataset.iloc[row_id]
        current_context_text = row["current_state"]
        goal_text = row["goal_text"]
        possible_actions = row["possible_actions"].split(".")
        domain_intro = task_config["domain_intro"]
        
        model_return = chain.invoke({
            "domain_intro": domain_intro, "current_context_text": current_context_text, "goal_text": goal_text
        })
        
        index = model_return.find("THE NEXT BEST ACTION IS: ")
        if index == -1:
            action = "no action"
            action_possible = -1
        else:
            try:
                action = model_return.split("THE NEXT BEST ACTION IS: ")[-1].lower()
                action = action.split(".")[0]
                is_action = is_valid_action(action, task_config)
                if not is_action:
                    action = "no action"
                    action_possible = -1
                else:
                    action_possible = 1 if action in possible_actions else 0
            except:
                action = "no action"
                action_possible = -1
        
        action_possible_list.append(action_possible)
        model_return_list.append(model_return)
        action_list.append(action)
    
    dataset["model_return"] = model_return_list
    dataset["action"] = action_list
    dataset["action_possible"] = action_possible_list
    
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
