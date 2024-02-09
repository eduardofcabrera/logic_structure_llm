import itertools
import re
import numpy as np
import pandas as pd

from random import randint
from tqdm import tqdm
from typing import List, Tuple, Dict, Any

from sample_generator import SampleGenerator
from customer_sample_format import customer_json_format

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

variables_list = ["age", "sex", "height", "weight", "registration_time", "city"]
text_dict = {
    "age": {1: "is more than 45 years", 0: "is less than 45 years"},
    "sex": {0: "is male", 1: "is female"},
    "height": {
        1: "is more than 170 centimeters tall",
        0: "is less than 170 centimeters tall",
    },
    "weight": {1: "weighs more than 60 kilograms", 0: "weighs less than 60 kilograms"},
    "registration_time": {
        1: "has registered for more than 12 months",
        0: "has registered for less than 12 months",
    },
    "city": {0: "lives in the west coast", 1: "lives in the east coast"},
}


def get_rule_text_from_choice(
    variables: List[str], choice: Tuple[int], choice_id: int
) -> str:
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
        "registration_time": """registragion_time (time in months since the customer registered): {registration_time}\n""",
        "city": """city (customer city): {city}\n""",
    }

    variables_templates = [customer_templates[variable] for variable in variables]

    customer_prompt_template = """Given the customer informations below:\n""" + "".join(
        variables_templates
    )

    return customer_prompt_template


def get_prompt(variables: List[str], choices: List[Tuple[int]]):
    system_prompt = SystemMessage(
        content="You are a system that gets an information of a customer and follow some rules to take a specific action for each customer."
    )
    customer_prompt_template = get_customer_prompt_template(variables)
    rules_prompt_template = get_rules_text_from_choices(variables, choices)
    order_prompt_template = (
        """Return only the number of the action chosen, nothing more."""
    )

    return (
        system_prompt
        + customer_prompt_template
        + rules_prompt_template
        + order_prompt_template
    )


def get_prompt_extract_information(variables: List[str]):

    system_prompt = SystemMessage(
        content="You are a system that extracts customer information and output it in JSON format."
    )
    customer_prompt_template = get_customer_prompt_template(variables)
    order_prompt_template = """Output only the customer information in JSON format. Use a dict with each key being the name of the variable."""

    return system_prompt + customer_prompt_template + order_prompt_template


def get_chain_extract_information(variables: List[str]):

    prompt = get_prompt_extract_information(variables)

    model = ChatOpenAI()
    json_output_parser = JsonOutputParser()

    chain = prompt | model | json_output_parser

    return chain


def get_chain(variables: List[str], choices: List[Tuple[int]]):

    prompt = get_prompt(variables, choices)

    model = ChatOpenAI()
    str_output_parser = StrOutputParser()

    chain = prompt | model | str_output_parser

    return chain


def get_inference_extract_information(
    n_variables: int, variables: List[str]
) -> Tuple[Dict, int, int]:

    customer_sample_generator = SampleGenerator(customer_json_format)
    customer = customer_sample_generator.generate_sample()

    choices = list(itertools.product([0, 1], repeat=n_variables))
    choice = tuple([customer[variable][1] for variable in variables])
    choice_id = choices.index(choice) + 1

    chain = get_chain_extract_information(variables)

    customer_json = {variable: customer[variable][0] for variable in variables}

    customer_information = chain.invoke(customer_json)

    deterministic_choice = customer_sample_generator.get_true_choice_from_sampe(
        customer_information
    )
    deterministic_choice_id = choices.index(deterministic_choice) + 1

    return customer_json, choice_id, deterministic_choice_id


def get_inference(
    n_variables: int,
    variables: List[str],
) -> Tuple[Dict, int, int]:

    customer_sample_generator = SampleGenerator(customer_json_format)
    customer = customer_sample_generator.generate_sample()

    choices = list(itertools.product([0, 1], repeat=n_variables))
    choice = tuple([customer[variable][1] for variable in variables])
    choice_id = choices.index(choice)

    chain = get_chain(variables, choices)

    customer_json = {variable: customer[variable][0] for variable in variables}

    inference_action = chain.invoke(customer_json)
    inference_action = [int(s) for s in re.findall(r"\b\d+\b", inference_action)][0]

    return customer_json, choice_id + 1, inference_action


def main_(n_variables: int, n_samples: int):

    variables = variables_list[:n_variables]

    df = pd.DataFrame([])

    for _ in tqdm(range(n_samples)):

        customer_json, correct_choice_id, inference_choice_id = get_inference(
            n_variables, variables
        )

        customer_json["correct_choice_id"] = correct_choice_id
        customer_json["inference_choice_id"] = inference_choice_id

        df = pd.concat([df, pd.DataFrame([customer_json])])

    df.to_csv(f"experiments/{n_variables}_{n_samples}.csv", index=False)

    acc = (df["correct_choice_id"] == df["inference_choice_id"]).sum() / (
        df["correct_choice_id"]
    ).shape[0]

    print(n_variables, acc)

    return


def main(n_variables: int):

    variables = variables_list[:n_variables]
    customer_json_format["variables"] = {
        variable: customer_json_format["variables"][variable] for variable in variables
    }

    customer_json, correct_choice_id, deterministic_choice_id = (
        get_inference_extract_information(n_variables, variables)
    )

    print(correct_choice_id, deterministic_choice_id)


if __name__ == "__main__":
    # n_variables_list = [1, 2, 3, 4, 5, 6]
    # for n_variables in n_variables_list:
    #    main(n_variables, 100)
    main(6)
