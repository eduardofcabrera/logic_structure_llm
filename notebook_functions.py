from pathlib import Path
import pandas as pd
import numpy as np
import json
import random


def json_to_df(json_file: str) -> pd.DataFrame:
    with open(json_file) as f:
        data = json.load(f)
        f.close()
    instance_id_list = []
    goal_achieved_list = []
    content_list = []
    actions_text_list = []
    actions_possible_list = []
    n_actions_list = []
    for instance_id, value in data.items():
        value = value["chat_with_possible_actions"]
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
            "content": content,
            "actions_text": actions_text_list,
            "actions_possible": actions_possible_list,
            "n_actions": n_actions_list,
        }
    )

    return df


def json_to_df_without_checking_actions(json_file: str) -> pd.DataFrame:
    with open(json_file) as f:
        data = json.load(f)
        f.close()
    instance_id_list = []
    goal_achieved_list = []
    content_list = []
    actions_text_list = []
    n_actions_list = []
    for instance_id, value in data.items():
        value = value["chat_with_possible_actions"]
        goal_achieved = value["goal_achieved"]
        content = value["content"]
        actions = value["actions"]
        actions_text = [action for action in actions]
        n_actions = len(actions_text)
        actions_text = ".".join(actions_text)
        instance_id_list.append(instance_id)
        goal_achieved_list.append(goal_achieved)
        content_list.append(content)
        actions_text_list.append(actions_text)
        n_actions_list.append(n_actions)

    df = pd.DataFrame(
        {
            "instance_id": instance_id_list,
            "goal_achieved": goal_achieved_list,
            "content": content,
            "actions_text": actions_text_list,
            "n_actions": n_actions_list,
        }
    )

    return df


def all_possible_actions(actions_possible: str):
    if isinstance(actions_possible, float):
        if actions_possible == 0:
            return False
        return True
    actions_possible = actions_possible.split(".")
    if "0" in actions_possible:
        return False
    return True


def pre_proc_df(df: pd.DataFrame) -> pd.DataFrame:
    df["all_possible_actions"] = df["actions_possible"].apply(all_possible_actions)
    df["correct_response"] = df["goal_achieved"] & df["all_possible_actions"]
    return df


def get_acc(df: pd.DataFrame) -> float:
    return df["correct_response"].sum() / df.shape[0]


def get_n_actions_from_plan(plan: str) -> int:
    return len(plan.split("\n")) - 1


def get_ground_truth_df(ground_truth_file: str) -> pd.DataFrame:
    with open(ground_truth_file) as f:
        data = json.load(f)
        f.close()
    ground_truth_plan_list = [value["ground_truth_plan"] for value in data["instances"]]
    instance_id_list = [value["instance_id"] for value in data["instances"]]
    df = pd.DataFrame(ground_truth_plan_list, columns=["ground_truth_plan"])
    df["instance_id"] = instance_id_list
    df["ground_truth_n_actions"] = df["ground_truth_plan"].apply(
        get_n_actions_from_plan
    )
    return df


def pre_proc_ground_truth(
    df: pd.DataFrame, df_ground_truth: pd.DataFrame
) -> pd.DataFrame:
    df["instance_id"] = df["instance_id"] + 2
    df = df.merge(df_ground_truth, on="instance_id")
    return df


def get_mean_n_actions(df):
    return df[df["correct_response"] == True]["ground_truth_n_actions"].mean()


def get_ground_truth_n_actions(df):
    n_actions = df[df["correct_response"] == True]["ground_truth_n_actions"]
    n_actions += np.random.randn(n_actions.shape[0]) / 10
    return n_actions.to_list()


def get_all_ground_truth_n_actions(df):
    n_actions = df["ground_truth_n_actions"]
    n_actions += np.random.randn(n_actions.shape[0]) / 10
    return n_actions.to_list()


def get_n_actions(df):
    n_actions = df[df["correct_response"] == True]["n_actions"]
    n_actions += np.random.randn(n_actions.shape[0]) / 10
    return n_actions.to_list()


def get_all_n_actions(df):
    n_actions = df["n_actions"]
    n_actions += np.random.randn(n_actions.shape[0]) / 10
    return n_actions.to_list()


def get_analysis_from_folder(folder_path: str, ground_truth_df: pd.DataFrame):
    folder_path = Path(folder_path)
    csv_files = list(folder_path.glob("*.csv"))
    csv_types = [
        "only_prompt_g",
        "iterative_actions_g",
        "only_prompt_iterative_g",
        "chat_g",
        "chat_with_possible_actions_g",
        "chat_random_choice_g",
    ]
    df_list = []
    for i, csv_type in enumerate(csv_types):
        csv = [csv for csv in csv_files if csv_type in csv.stem][0]
        df = pd.read_csv(csv)
        if i in [0, 1, 2]:
            df = pre_proc_df(df)
        else:
            df["correct_response"] = df["goal_achieved"]
        df = pre_proc_ground_truth(df, ground_truth_df)
        df_list.append(df)
    return df_list


CSV_types = [
    "only_prompt_b",
    "only_prompt_iterative_b",
    "iterative_actions_b",
    "chat_b",
    "chat_with_possible_actions_b",
    "chat_random_choice_b",
    "chat_with_possible_actions_feedback_b",
    "chat_with_possible_actions_dist_1_b",
    "chat_with_possible_actions_dist_1_random_b",
]


def method_number_to_name(method_number: int) -> str:
    if method_number == 0:
        return "Full Plan Prompt"
    if method_number == 1:
        return "Validation Full Plan Prompt"
    if method_number == 2:
        return "Iterative Actions"
    if method_number == 3:
        return "Validation Iterative Actions"
    if method_number == 4:
        return "Possible Actions"
    if method_number == 5:
        return "Possible Actions Random"
    if method_number == 6:
        return "Possible Actions Loop Feedback"
    if method_number == 7:
        return "Possible Actions Depth-1"
    if method_number == 8:
        return "Possible Actions Depth-1 Random"


def get_balanced_df(df: pd.DataFrame) -> pd.DataFrame:
    unique_ground_truth = df["ground_truth_n_actions"].unique()
    n_instances_id_list = {}
    for unique in unique_ground_truth:
        df_ = df[df["ground_truth_n_actions"] == unique]
        n_instances_id = df_["instance_id"].unique().shape[0]
        n_instances_id_list[unique] = n_instances_id
    n_instances_id_min = min(n_instances_id_list.values())

    for unique in unique_ground_truth:
        df_ = df[df["ground_truth_n_actions"] == unique]
        unique_instances_ids = list(df_["instance_id"].unique())
        instances_ids_sample = random.sample(unique_instances_ids, k=n_instances_id_min)
        n_instances_id_list[unique] = instances_ids_sample

    df_balanced = pd.DataFrame([])
    for unique in unique_ground_truth:
        df_ = df[df["ground_truth_n_actions"] == unique]
        df_ = df_[df_["instance_id"].isin(n_instances_id_list[unique])]
        df_balanced = pd.concat([df_balanced, df_])
    return df_balanced


def get_n_few_shot_actions(content: str) -> int:
    actions = content.split("[PLAN]")[1].split("[PLAN END]")[0].split("\n")
    return len(actions) - 2


def get_df_from_folder(folder_path):
    csv_types = [
        "only_prompt_b",
        "iterative_actions_b",
        "only_prompt_iterative_b",
        "chat_b",
        "chat_with_possible_actions_b",
        "chat_random_choice_b",
        "chat_with_possible_actions_loop_b",
        "chat_with_possible_actions_feedback_b",
        "chat_with_possible_actions_dist_1_random_b",
    ]
    csv_types = CSV_types
    folder_path = Path(folder_path)
    csv_files = folder_path.glob("*.csv")
    df_concat = pd.DataFrame([])
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        file_name = csv_file.stem
        n_run = file_name[0]
        df_cat = [csv_type in file_name for csv_type in csv_types].index(True)
        if df_cat in [0, 1, 2]:
            df = pre_proc_df(df)
        else:
            df["correct_response"] = df["goal_achieved"]
        df["n_run"] = n_run
        df["method"] = df_cat
        df_concat = pd.concat([df_concat, df])
    df = df_concat
    df["method_name"] = df["method"].apply(method_number_to_name)
    return df


def iterations_count_from_validation_full_prompt(content: str) -> int:
    return content.count("Write only:")
