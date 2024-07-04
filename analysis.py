from parse_args import parse_args
import yaml
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
from notebook_functions import *


def average_accuracy_plot(df: pd.DataFrame, model_name: str, image_folder: Path):
    acc_by_method = (
        df.groupby("method", as_index=False)["correct_response"].mean().round(3)
    )
    acc_by_method["method"] = acc_by_method["method"].apply(method_number_to_name)
    ax = sn.barplot(acc_by_method, x="correct_response", y="method", orient="h")
    ax.set_axisbelow(True)
    ax.xaxis.grid(True)
    ax.bar_label(ax.containers[0], fontsize=10)
    ax.set_xlim([0, max(acc_by_method["correct_response"]) + 0.05])
    ax.set_xlabel("Accuracy")
    ax.set_ylabel("Method")
    ax.set_title(f"Average accuracy by method for - {model_name}")

    plt.savefig(image_folder / "average_accuracy.png", bbox_inches="tight")


def average_accuracy_by_n_actions(
    df: pd.DataFrame, model_name: str, image_folder: Path
):

    acc_by_method_gd_actions = df.groupby(
        ["method", "ground_truth_n_actions"], as_index=False
    )["correct_response"].mean()
    acc_by_method_gd_actions["correct_response"] = acc_by_method_gd_actions[
        "correct_response"
    ].round(3)
    acc_by_method_gd_actions["method"] = acc_by_method_gd_actions["method"].apply(
        method_number_to_name
    )
    acc_by_method_gd_actions = df.groupby(
        ["method", "ground_truth_n_actions"], as_index=False
    )["correct_response"].mean()
    acc_by_method_gd_actions["correct_response"] = acc_by_method_gd_actions[
        "correct_response"
    ].round(3)
    acc_by_method_gd_actions["method"] = acc_by_method_gd_actions["method"].apply(
        method_number_to_name
    )
    ax = sn.catplot(
        acc_by_method_gd_actions,
        col="method",
        y="correct_response",
        x="ground_truth_n_actions",
        kind="bar",
        col_wrap=3,
    )
    ax.figure.subplots_adjust(top=0.9)
    ax.figure.suptitle(f"Average accuracy by method - {model_name}")
    method_names = list(map(method_number_to_name, [0, 1, 2, 3, 4, 5, 6]))
    for i, ax in enumerate(ax.axes_dict.values()):
        ax.set_title(method_names[i])
        ax.set_axisbelow(True)
        ax.yaxis.grid(True)
        ax.bar_label(ax.containers[0], fontsize=10)
        ax.set_xlabel("Optimal number of Actions")
        ax.set_ylabel("Accuracy")

    plt.savefig(image_folder / "average_accuracy_n_actions.png", bbox_inches="tight")


def iteractions_to_achieve_goal(df: pd.DataFrame, model_name: str, image_folder: Path):
    data = df[df["correct_response"] == True]

    data_iterations = data[data["method"].isin([1, 3, 4, 5])]
    data_iterations["iterations"] = data_iterations["n_actions"]

    data_validation_full_plan = data[data["method"] == 2]
    data_validation_full_plan["iterations"] = data_validation_full_plan[
        "content"
    ].apply(iterations_count_from_validation_full_prompt)

    data_full_plan = data[data["method"] == 0]
    data_full_plan["iterations"] = 1

    data = pd.concat([data_iterations, data_validation_full_plan, data_full_plan])

    method_sum = data.groupby("method", as_index=False)["iterations"].count()
    method_sum["method"] = method_sum["method"].apply(method_number_to_name)
    iterations_by_method_gd_actions = data.groupby(
        ["method", "iterations"], as_index=False
    )["correct_response"].count()
    iterations_by_method_gd_actions["method"] = iterations_by_method_gd_actions[
        "method"
    ].apply(method_number_to_name)

    frequencies = []
    for i in range(iterations_by_method_gd_actions.shape[0]):
        row = iterations_by_method_gd_actions.iloc[i]
        method = row["method"]
        sum_iterations = method_sum[method_sum["method"] == method][
            "iterations"
        ].values[0]
        frequency = row["correct_response"] / sum_iterations
        frequencies.append(frequency)

    iterations_by_method_gd_actions["correct_response"] = frequencies

    ax = sn.catplot(
        iterations_by_method_gd_actions,
        col="method",
        y="correct_response",
        x="iterations",
        kind="bar",
        col_wrap=3,
    )
    ax.figure.subplots_adjust(top=0.9)
    ax.figure.suptitle(f"Number of Iterations to Achieve the Goal - {model_name}")
    method_names = list(map(method_number_to_name, sorted(df["method"].unique())))
    for i, ax in enumerate(ax.axes_dict.values()):
        ax.set_title(method_names[i])
        ax.set_axisbelow(True)
        ax.yaxis.grid(True)
        ax.set_xlabel("Number of Iterations")
        ax.set_ylabel("Frequency")

    plt.savefig(image_folder / "iterations_to_achieve_goal.png", bbox_inches="tight")


def distance_to_ground_truth(df: pd.DataFrame, model_name: str, image_folder: Path):
    data = df[df["correct_response"] == False]
    data = (
        data.groupby(["method", "ground_truth_n_actions"], as_index=False)[
            "distance_to_ground_truth"
        ]
        .agg(["mean", "std", "count", "median"])
        .dropna()
        .round(3)
    )
    data["method"] = data["method"].apply(method_number_to_name)

    ax = sn.catplot(
        data, col="method", y="mean", x="ground_truth_n_actions", kind="bar", col_wrap=3
    )
    ax.figure.subplots_adjust(top=0.9)
    ax.figure.suptitle(
        f"Distance between Predicted Plan and Ground Truth Plan - {model_name}"
    )
    method_names = list(map(method_number_to_name, sorted(df["method"].unique())))
    for i, ax in enumerate(ax.axes_dict.values()):
        ax.set_title(method_names[i])
        ax.bar_label(ax.containers[0], fontsize=10)
        ax.set_axisbelow(True)
        ax.yaxis.grid(True)
        ax.set_xlabel("Optimal number of Actions")
        ax.set_ylabel("Mean Distance (Number of Actions)")

    plt.savefig(image_folder / "distance_to_ground_truth.png", bbox_inches="tight")


def distance_to_initial(df: pd.DataFrame, model_name: str, image_folder: Path):
    data = df[df["correct_response"] == False]
    data = (
        data.groupby(["method", "ground_truth_n_actions"], as_index=False)[
            "distance_to_init"
        ]
        .agg(["mean", "std", "count", "median"])
        .dropna()
        .round(3)
    )
    data["method"] = data["method"].apply(method_number_to_name)

    ax = sn.catplot(
        data, col="method", y="mean", x="ground_truth_n_actions", kind="bar", col_wrap=3
    )
    ax.figure.subplots_adjust(top=0.9)
    ax.figure.suptitle("Distance between Predicted Plan and Initial State (Mixtral)")
    method_names = list(map(method_number_to_name, sorted(df["method"].unique())))
    for i, ax in enumerate(ax.axes_dict.values()):
        ax.set_title(method_names[i])
        ax.bar_label(ax.containers[0], fontsize=10)
        ax.set_axisbelow(True)
        ax.yaxis.grid(True)
        ax.set_xlabel("Optimal number of Actions")
        ax.set_ylabel("Mean Distance (Number of Actions)")

    plt.savefig(image_folder / "distance_to_init.png", bbox_inches="tight")


def make_analysis(config_run):
    results_folder = config_run["results_folder"]
    model_name = config_run["model_name"]
    results_folder = Path(results_folder)
    metrics_file = f"metrics_results/{results_folder.stem}.csv"
    image_folder = Path("images") / results_folder.stem
    image_folder.mkdir(exist_ok=True)

    df = pd.read_csv(metrics_file)

    average_accuracy_plot(df, model_name, image_folder)
    average_accuracy_by_n_actions(df, model_name, image_folder)
    iteractions_to_achieve_goal(df, model_name, image_folder)
    distance_to_ground_truth(df, model_name, image_folder)
    distance_to_initial(df, model_name, image_folder)


if __name__ == "__main__":
    args = parse_args()
    config_file = args.config
    with open(config_file) as f:
        config_run = yaml.safe_load(f)
        f.close()

    make_analysis(config_run)
