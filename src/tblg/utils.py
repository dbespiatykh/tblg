"""Various helper functions"""
import codecs
import datetime
import logging
import os
import os.path

import pandas as pd
import rich_click as click
from rich import print as rprint
from rich.logging import RichHandler
from rich.prompt import Prompt
from tabulate import tabulate

FORMAT = "%(message)s"
rhandler = RichHandler(
    level=logging.NOTSET,
    show_level=True,
    show_path=False,
    show_time=True,
    omit_repeated_times=False,
)

logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[rhandler])
log = logging.getLogger("rich")


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

    if not os.path.dirname(output):
        output = os.path.join(os.getcwd(), output)

    try:
        if os.path.exists(output):
            while True:
                user_input = Prompt.ask(
                    f"[yellow bold]File[/] [cyan italic]{output}[/] [yellow bold]already exists.\n"
                    f"Do you want to overwrite it? (y/n) [dim] Press [italic]ENTER[/] to exit",
                )
                if user_input.lower() == "y":
                    rprint(f"[yellow bold]Overwriting[/] [italic]{output}")
                    break
                elif user_input.lower() == "n":
                    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    new_output = f"{now}_{os.path.basename(output)}"
                    output_dir = os.path.dirname(output)
                    if not output_dir:
                        output_dir = os.getcwd()
                    new_output = os.path.join(output_dir, new_output)
                    new_output = os.path.splitext(new_output)[0] + ".tsv"
                    results.to_csv(new_output, index=False, sep="\t")
                    rprint(f"[yellow bold]Saving as[/] [italic]{new_output}")
                    return
                elif user_input == "":
                    raise KeyboardInterrupt
                else:
                    rprint(
                        "[red bold]Invalid input.[/] [yellow]Please enter [italic]'y'[/] or [italic]'n'[/]."
                    )

        os.makedirs(os.path.dirname(output), exist_ok=True)

        ext = os.path.splitext(output)[1]
        if ext == ".csv":
            results.to_csv(output, index=False)
        elif ext == ".tsv" or ext == ".txt":
            results.to_csv(output, index=False, sep="\t")
        else:
            raise SystemExit("Output file must have 'txt', 'tsv', or 'csv' extension")

    except OSError as e:
        if e.errno == 30:
            log.error(
                "File cannot be created at this path. Read-only file system. Please check your file system permissions."
            )
        else:
            raise e


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
        rprint("[red bold]ATTENTION[/]: [italic]No lineages were called!")
    else:
        table = tabulate(results, headers=headers, tablefmt="fancy_grid")
        print(f"\n{table}")


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
            rprint(
                "[red bold]ATTENTION[/]: [italic]Please provide one or more VCF files to process"
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
            rprint(
                "[red bold]ATTENTION[/]: [italic]Output file must have 'txt', 'tsv', or 'csv' extension",
            )
            click.echo(self.ctx.get_help())
            self.ctx.exit()

        elif self.output:
            rprint(f"[yellow bold]Writing results to[/] [cyan italic]{self.output}[/]")


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
