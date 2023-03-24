"""Various helper functions"""
import codecs
import os
import os.path

import click
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
    Print a dataframe containing results to the console in a formatted table.

    Args:
    ____
        results (pandas.DataFrame): A DataFrame containing the results to be printed.

    Returns:
    _______
        None.
    """
    headers = ["Sample", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
    if results.empty:
        click.secho("ATTENTION: No lineages were called!", bold=True)
    else:
        table = tabulate(results, headers=headers, tablefmt="grid")
        print(table)


class InputOutputValidator:
    """Class to validate input and output"""

    def __init__(self, ctx, vcf_files, output):
        """
        Initialize InputOutputValidator.

        Parameters:
        -----------
        ctx : click.Context
            The click context object.
        vcf_files : tuple
            Tuple containing VCF files.
        output : str
            File path to write output to.
        """
        self.ctx = ctx
        self.vcf_files = vcf_files
        self.output = output

    def validate_input(self):
        """
        Validate input.

        Raises:
        -------
        click.exceptions.ClickException:
            If no VCF files are provided and help flag is not set.
        """
        if not self.vcf_files and not self.ctx.params.get("help"):
            click.secho(
                "ATTENTION: Please provide one or more VCF files to process\n",
                bold=True,
            )
            click.echo(self.ctx.get_help())
            self.ctx.exit()

    def validate_output(self):
        """
        Validate output.

        Raises:
        -------
        click.exceptions.ClickException:
            If output file doesn't have valid extension or help flag is set.
        """
        if self.output and not self.output.endswith((".txt", ".tsv", ".csv")):
            click.secho(
                "ATTENTION: Output file must have extension 'txt', 'tsv', or 'csv'\n",
                bold=True,
            )
            click.echo(self.ctx.get_help())
            self.ctx.exit()

        elif self.output:
            click.secho(f"Writing results to {self.output}", bold=True)


def read(rel_path):
    """
    Read file at the specified path.

    Parameters:
    -----------
    rel_path : str
        Path to the file relative to this one.

    Returns:
    --------
    str:
        Contents of the file.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    """
    Extract version number from the specified file.

    Parameters:
    -----------
    rel_path : str
        Path to the file relative to this one.

    Returns:
    --------
    str:
        The version number.
    """
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")
