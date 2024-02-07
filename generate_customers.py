import itertools
import re
import numpy as np

from random import randint
from tqdm import tqdm
from typing import List, Tuple, Dict

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

variables_list = ["age", "sex", "height", "weight", "registration_time", "city"]
text_dict = {
    "age": {0: "is more than 45 years", 1: "is less than 45 years"},
    "sex": {0: "is male", 1: "is female"},
    "height": {0: "is more than 170 centimeters tall", 1: "is less than 170 centimeters tall"},
    "weight": {0: "weighs more than 60 kilograms", 1: "weighs less than 60 kilograms"},
    "registration_time": {0: "has registered for more than 12 months", 1: "has registered for less than 12 months"},
    "city": {0: "lives in the west coast", 1: "lives in the east coast"},
}

def get_age() -> int:
    age = 45
    while age == 45:
        age = randint(10, 80)
    if age > 45:
        return age, 0
    return age, 1

def get_sex() -> str:
    choices = ["male", "female"]
    _id = randint(0, 1)
    return choices[_id], _id

def get_height() -> int:
    height = 170
    while height == 170:
        height = randint(130, 210)
    if height > 170:
        return height, 0
    return height, 1

def get_weight() -> int:
    weight = 60
    while weight == 60:
        weight = randint(20, 100)
    if weight > 60:
        return weight, 0
    return weight, 1

def get_registration_time() -> int:
    registration_time = 12
    while registration_time == 12:
        registration_time = randint(0, 24)
    if registration_time > 12:
        return registration_time, 0
    return registration_time, 1

def get_city():
    choices = ["San Francisco", "Los Angeles", "San Diego", "New York", "Boston", "Washington"]
    choices_id = [0, 0, 0, 1, 1, 1]
    
    _id = randint(0, 5)
    return choices[_id], choices_id[_id]
    
def get_rule_text_from_choice(variables: List[str], choice: Tuple[int], choice_id: int) -> str:
    text = f"Action {choice_id+1}. If the customer "
    len_choice = len(choice)
    for i, variable in enumerate(variables):
        text += text_dict[variable][choice[i]]
        if i < len_choice - 2:
            text += ", "
        elif i == len_choice - 2:
            text += " and "
        else:
            text += "."
            
    return text

def get_rules_text_from_choices(variables: List[str], choices: List[Tuple[int]]) -> str:
    
    text = "Choose one, and only one, action between this set of rules:\n"
    for choice_id, choice in enumerate(choices):
        text += get_rule_text_from_choice(variables, choice, choice_id) + "\n"
    
    return text

def get_customer_prompt_template(variables: List[str]):
    
    customer_templates = {
        "age": """age (customer age in years): {age}\n""",
        "sex": """sex (customer sex): {sex}\n""",
        "height": """height (customer height in centimeters): {height}\n""",
        "weight": """weight (customer weight in kilograms): {weight}\n""",
        "registration_time": """registragion time (time in months since the customer registered): {registration_time}\n""",
        "city": """city (customer city): {city}\n""" 
    }
    
    variables_templates = [customer_templates[variable] for variable in variables]
    
    customer_prompt_template = """Given the customer informations below:\n""".join(variables_templates)
    
    return customer_prompt_template

def get_prompt(variables: List[str], choices: List[Tuple[int]]):
    system_prompt = SystemMessage(content="You are a system that gets an information of a customer and follow some rules to take a specific action for each customer.")
    customer_prompt_template = get_customer_prompt_template(variables)
    rules_prompt_template = get_rules_text_from_choices(variables, choices)
    order_prompt_template = """Return only the number of the action choosen, nothing more."""
    
    return (
        system_prompt + customer_prompt_template + rules_prompt_template + order_prompt_template
    )

def get_chain(variables: List[str], choices: List[Tuple[int]]):
    
    prompt = get_prompt(variables, choices)
    
    model = ChatOpenAI()
    str_output_parser = StrOutputParser()
    
    chain = (
        prompt
        | model
        | str_output_parser
    )
    
    return chain
    
def generate_customer() -> Dict[str: Tuple]:
    customer = {
        "age": get_age(),
        "sex": get_sex(),
        "height": get_height(),
        "weight": get_weight(),
        "registration_time": get_registration_time(),
        "city": get_city()
    }
    
    return customer

def get_inference(n_variables: int, variables: List[str], ) -> Tuple[int, int]:
    
    customer = generate_customer()
    
    choices = list(itertools.product([0, 1], repeat=n_variables))
    choice = tuple([customer[variable][1] for variable in variables])
    choice_id = choices.index(choice)
    
    chain = get_chain(variables, choices)
    
    customer_json = {variable: customer[variable] for variable in variables}

    action = chain.invoke(customer_json)
    action_id = [int(s) for s in re.findall(r'\b\d+\b', action)][0]
    
    return choice_id+1, action_id

def main(n_variables: int):
    
    variables = variables_list[:n_variables]
    
    correct_actions = []
    returned_actions = []
    
    for _ in tqdm(range(50)):
    
        choice_id, action_id = get_inference(n_variables, variables)
        
        correct_actions.append(choice_id)
        returned_actions.append(action_id)
        
    
    correct_actions = np.array(correct_actions)
    returned_actions = np.array(returned_actions)
    
    print((correct_actions == returned_actions).sum() / len(correct_actions))
    
    return 

if __name__ == "__main__":
    main(2)

