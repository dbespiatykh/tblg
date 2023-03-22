"""Output related functions"""
import os

import pandas as pd
from tabulate import tabulate


def combine_results(results_list):
    """
    Combine a list of dataframes containing results into a single dataframe
    """
    if not results_list:
        return pd.DataFrame()

    results = pd.concat(results_list, ignore_index=True)
    results = results.sort_values(
        by=["level_1", "level_2", "level_3", "level_4", "level_5"]
    ).reset_index(drop=True)

    return results


def write_results_to_file(results, output):
    """
    Write a dataframe containing results to a file in CSV or TSV format
    """
    if not output:
        return

    os.makedirs(os.path.dirname(output), exist_ok=True)

    ext = os.path.splitext(output)[1]
    if ext == ".csv":
        results.to_csv(output, index=False)
    elif ext == ".tsv" or ext == ".txt":
        results.to_csv(output, index=False, sep="\t")
    else:
        raise SystemExit("Output file must have extension 'txt', 'tsv', or 'csv'")


def print_results(results):
    """
    Print a dataframe containing results to the console in a formatted table
    """
    headers = ["Sample", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
    if not results.empty:
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        print("No lineages were called!")
