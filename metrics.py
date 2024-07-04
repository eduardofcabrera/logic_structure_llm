from pathlib import Path
import yaml
from collections import deque
import networkx as nx
import copy

from tqdm import tqdm
import pandas as pd

from src.blocksworld_import import Blocksworld
from notebook_functions import get_df_from_folder

from parse_args import parse_args


def get_first_letter(string: str):
    return string[0]


def state_to_string(state: list):
    string = ""
    predicates_strings = []
    for predicate in state:
        predicate_string = str(predicate)[1:].split(" ")
        predicate_string = "".join(map(get_first_letter, predicate_string))
        predicates_strings.append(predicate_string)
    predicates_strings.sort()
    return "_".join(predicates_strings)


class State_Hashtable:
    def __init__(self):
        self.table = {}
        self.length = 0

    def add(self, state, parent_state, depth):
        state_string = state_to_string(state.problem_state.current_state_predicate_list)
        if not self.table.get(state_string, None):
            self.table[state_string] = (self.length, state, parent_state, depth)
            self.length += 1

    def get(self, state):
        state_string = state_to_string(state.problem_state.current_state_predicate_list)
        if state_string in self.table:
            return self.table[state_string]
        return None

    def is_in(self, state):
        state_string = state_to_string(state.problem_state.current_state_predicate_list)

        return self.table.get(state_string, None) != None

    def __len__(self):
        return len(self.table)

    def __str__(self):
        return str(self.table)


def BFS(engine, depth=-1):
    G = nx.DiGraph()
    q = deque()
    q.append(engine)
    hash_table = State_Hashtable()
    hash_table.add(engine, None, 0)
    G.add_node(hash_table.get(engine)[0], engine=engine)
    while len(q) != 0:
        current_engine = q.popleft()
        if depth != -1 and hash_table.get(current_engine)[3] >= depth:
            return None, hash_table, G
        if current_engine.problem_state.goal_reached():
            return current_engine, hash_table, G
        possible_actions = current_engine.problem_state.get_all_possible_actions()
        for possible_action in possible_actions:
            new_engine = copy.deepcopy(current_engine)
            new_engine.problem_state.take_action(*possible_action)
            # G.add_node(hash_table.get(new_engine)[0], engine=new_engine)
            # G.add_edge(hash_table.get(current_engine)[0], hash_table.get(new_engine)[0], action=current_engine.action_to_text(possible_action))
            if not hash_table.is_in(new_engine):
                hash_table.add(
                    new_engine, current_engine, hash_table.get(current_engine)[3] + 1
                )
                q.append(new_engine)
                G.add_node(hash_table.get(new_engine)[0], engine=new_engine)
                G.add_edge(
                    hash_table.get(current_engine)[0],
                    hash_table.get(new_engine)[0],
                    action=current_engine.action_to_text(possible_action),
                )
            if new_engine.problem_state.goal_reached():
                return new_engine, hash_table, G

    return None, hash_table, G


def BFS_2(engine, first_engine, depth=-1):
    G = nx.DiGraph()
    q = deque()
    q.append(engine)
    hash_table = State_Hashtable()
    hash_table.add(engine, None, 0)
    G.add_node(hash_table.get(engine)[0], engine=engine)
    while len(q) != 0:
        current_engine = q.popleft()
        if depth != -1 and hash_table.get(current_engine)[3] >= depth:
            return None, hash_table, G
        if state_to_string(
            current_engine.problem_state.current_state_predicate_list
        ) == state_to_string(first_engine.problem_state.current_state_predicate_list):
            return current_engine, hash_table, G
        possible_actions = current_engine.problem_state.get_all_possible_actions()
        for possible_action in possible_actions:
            new_engine = copy.deepcopy(current_engine)
            new_engine.problem_state.take_action(*possible_action)
            # G.add_node(hash_table.get(new_engine)[0], engine=new_engine)
            # G.add_edge(hash_table.get(current_engine)[0], hash_table.get(new_engine)[0], action=current_engine.action_to_text(possible_action))
            if not hash_table.is_in(new_engine):
                hash_table.add(
                    new_engine, current_engine, hash_table.get(current_engine)[3] + 1
                )
                q.append(new_engine)
                G.add_node(hash_table.get(new_engine)[0], engine=new_engine)
                G.add_edge(
                    hash_table.get(current_engine)[0],
                    hash_table.get(new_engine)[0],
                    action=current_engine.action_to_text(possible_action),
                )
            if new_engine.problem_state.goal_reached():
                return new_engine, hash_table, G

    return None, hash_table, G


def get_path_to_goal(hash_table, G, goal_state):
    state_sequence = []
    actions_sequence = []

    state_id, current_state, parent_state, _ = hash_table.get(goal_state)
    state_sequence.append(current_state)
    while parent_state != None:
        child_state_id = state_id
        state_id, current_state, parent_state, _ = hash_table.get(parent_state)
        action = G.get_edge_data(state_id, child_state_id)["action"]
        actions_sequence.append(action)
        state_sequence.append(current_state)
        current_state = parent_state

    return state_sequence[::-1], actions_sequence[::-1]


def apply_plan(engine: Blocksworld, plan, actions_possible, method):
    repeated_states = 0
    states_hash = set()
    states_hash.add(hash(engine.current_state_to_text()))
    try:
        actions = plan.split(".")
        actions_possible = actions_possible.split(".")
    except:
        return engine, repeated_states
    if method in [0, 1, 2]:
        if "0" in actions_possible:
            return engine, repeated_states
    for i, action in enumerate(actions):
        try:
            engine.take_action_from_text(action)
            action_possible = actions_possible[i]
            if action_possible == "1":
                hash_state = hash(engine.current_state_to_text())
                if hash_state in states_hash:
                    repeated_states += 1
                else:
                    states_hash.add(hash_state)
        except:
            pass
    return engine, repeated_states


def iteration_full_prompt(df):

    df_ = df[df["method"] == 0]
    df_["iter_mode"] = 0
    df_2 = df_.copy()
    df_2["iter_mode"] = 1

    df = pd.concat([df_, df_2])
    df["n_iterations"] = 1
    return df


def convert_iter_contents(row, dataset_folder, config_run):

    content = row["content"]
    plans_split = content.split("ai: ")[1:]
    n_iters = len(plans_split)
    if n_iters <= 5:
        return (
            row["content"],
            row["actions_text"],
            row["actions_possible"],
            row["all_possible_actions"],
            row["goal_achieved"],
            row["correct_response"],
            row["n_actions"],
        )

    fith_plan = plans_split[4]
    fith_plan = fith_plan.split("<plan>\n")[1].split("\n<\plan>")[0]
    actions = fith_plan.split("\n")

    instance_id = row["instance_id"]
    pddl_file = dataset_folder / f"instance_{instance_id}" / "pddl.pddl"
    config_run["pddl_file"] = pddl_file

    engine = Blocksworld(config_run)

    actions = {
        f"{i}": (action, engine.take_action_from_text(action))
        for i, action in enumerate(actions)
    }

    actions = {
        key: (value[0], value[1][0]) for key, value in actions.items() if value[1][1]
    }

    content_ = "human: ".join(content.split("human: ")[:6])
    actions_text = ".".join([value[0] for key, value in actions.items()])
    actions_possible = ".".join([str(int(value[1])) for key, value in actions.items()])
    all_possible_actions = all([value[1] for key, value in actions.items()])
    goal_reached = engine.problem_state.goal_reached()
    n_actions = len(actions_text.split("."))
    correct_response = goal_reached and all_possible_actions

    return (
        content_,
        actions_text,
        actions_possible,
        all_possible_actions,
        goal_reached,
        correct_response,
        n_actions,
    )


def iteration_validation_full_prompt(df, dataset_folder, config_run):
    df_ = df[df["method"] == 1]
    if df_.shape[0] == 0:
        return df_
    row = df_.iloc[0]

    content_list = []
    actions_text_list = []
    actions_possible_list = []
    all_possible_actions_list = []
    goal_reached_list = []
    correct_response_list = []
    n_actions_list = []

    for row in tqdm(range(df_.shape[0])):
        row = df_.iloc[row]
        (
            content,
            actions_text,
            actions_possible,
            all_possible_actions,
            goal_reached,
            correct_response,
            n_actions,
        ) = convert_iter_contents(row, dataset_folder, config_run)

        content_list.append(content)
        actions_text_list.append(actions_text)
        actions_possible_list.append(actions_possible)
        all_possible_actions_list.append(all_possible_actions)
        goal_reached_list.append(goal_reached)
        correct_response_list.append(correct_response)
        n_actions_list.append(n_actions)

    df_2 = df_.copy()
    df_2["content"] = content_list
    df_2["actions_text"] = actions_text_list
    df_2["actions_possible"] = actions_possible_list
    df_2["all_possible_actions"] = all_possible_actions_list
    df_2["goal_achieved"] = goal_reached_list
    df_2["correct_response"] = correct_response_list
    df_2["n_actions"] = n_actions_list

    df_2["iter_mode"] = 0
    df_["iter_mode"] = 1

    df = pd.concat([df_, df_2])
    df["n_iterations"] = df["content"].apply(lambda x: len(x.split("ai: ")[1:]))

    return df


def iteration_iterative_methods(df):
    df_ = df[df["method"].isin([2, 3, 4])]

    content_list = []
    actions_text_list = []
    actions_possible_list = []
    all_possible_actions_list = []
    goal_reached_list = []
    correct_response_list = []
    n_actions_list = []

    for i in range(df_.shape[0]):
        row = df_.iloc[i]
        if row["n_actions"] <= 10:
            content_list.append(row["content"])
            actions_text_list.append(row["actions_text"])
            actions_possible_list.append(row["actions_possible"])
            all_possible_actions_list.append(row["all_possible_actions"])
            goal_reached_list.append(row["goal_achieved"])
            correct_response_list.append(row["correct_response"])
            n_actions_list.append(row["n_actions"])
            continue

        content_ = "human: ".join(row["content"].split("human: ")[:10])
        actions_text = ".".join(row["actions_text"].split(".")[:10])
        actions_possible = ".".join(row["actions_possible"].split(".")[:10])
        goal_reached = False
        correct_response = False
        if row["method"] in [3, 4]:
            all_possible_actions = True
        else:
            all_possible_actions = all([int(x) for x in actions_possible.split(".")])
        n_actions = len(actions_text.split("."))

        content_list.append(content_)
        actions_text_list.append(actions_text)
        actions_possible_list.append(actions_possible)
        all_possible_actions_list.append(all_possible_actions)
        goal_reached_list.append(goal_reached)
        correct_response_list.append(correct_response)
        n_actions_list.append(n_actions)

    df_2 = df_.copy()
    df_2["content"] = content_list
    df_2["actions_text"] = actions_text_list
    df_2["actions_possible"] = actions_possible_list
    df_2["all_possible_actions"] = all_possible_actions_list
    df_2["goal_achieved"] = goal_reached_list
    df_2["correct_response"] = correct_response_list
    df_2["n_actions"] = n_actions_list

    df_2["iter_mode"] = 0
    df_["iter_mode"] = 1

    df = pd.concat([df_, df_2])

    df["n_iterations"] = df["n_actions"]
    return df


def get_metrics(config_run):

    results_folder = config_run["results_folder"]
    results_folder = Path(results_folder)
    dataset_folder = Path(config_run["dataset_folder"])
    df = get_df_from_folder(results_folder)

    df["actions_text"] = df["actions_text"].fillna("no_action")
    df["actions_possible"] = df["actions_possible"].fillna("0")

    df["all_possible_actions"] = True
    df["all_possible_actions"] = df["all_possible_actions"].fillna(True)

    # df = df[df["method"].isin([3, 4])]

    df_full_prompt = iteration_full_prompt(df)
    df_validation_full_prompt = iteration_validation_full_prompt(
        df, dataset_folder, config_run
    )

    df_iterative = iteration_iterative_methods(df)

    df = pd.concat([df_full_prompt, df_validation_full_prompt, df_iterative])

    distance_to_ground_truth = []
    distance_to_init = []
    repeated_states_list = []

    for i in tqdm(range(df.shape[0])):
        row = df.iloc[i]
        instance_id = row["instance_id"]
        pddl_file = dataset_folder / f"instance_{instance_id}" / "pddl.pddl"
        config_run["pddl_file"] = pddl_file
        predicted_plan = row["actions_text"]
        actions_possible = row["actions_possible"]
        method = row["method"]
        engine = Blocksworld(config_run)
        first_engine = copy.deepcopy(engine)
        engine, repeated_states = apply_plan(
            engine, predicted_plan, actions_possible, method
        )
        repeated_states_list.append(repeated_states)
        goal_text, hash_table, G = BFS(engine)
        goal_text_first, hash_table_first, G_first = BFS_2(engine, first_engine)
        _, plan_to_goal = get_path_to_goal(hash_table, G, goal_text)
        _, plan_to_init = get_path_to_goal(hash_table_first, G_first, goal_text_first)
        distance_to_ground_truth.append(len(plan_to_goal))
        distance_to_init.append(len(plan_to_init))

    df["distance_to_ground_truth"] = distance_to_ground_truth
    df["distance_to_init"] = distance_to_init
    df["repeated_states"] = repeated_states_list

    df.to_csv(f"metrics_results/{results_folder.stem}.csv", index=False)


if __name__ == "__main__":
    args = parse_args()
    config_file = args.config
    with open(config_file) as f:
        config_run = yaml.safe_load(f)
        f.close()

    get_metrics(config_run)
