"""
TbLG (Tuberculosis Lineage Genotyping)

A command-line tool to genotype Mycobacterium tuberculosis lineage from a VCF file

Author: Dmitry Bespiatykh
"""
import sys

import rich_click as click
from rich import print as rprint

from .barcoding import process_vcf_files
from .utils import (
    InputOutputValidator,
    combine_results,
    get_version,
    print_results,
    write_results_to_file,
)

version = get_version("__init__.py")

click.rich_click.MAX_WIDTH = 75
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.HEADER_TEXT = f"[blue bold]TbLG[/][dim] (Tuberculosis Lineage Genotyping)[cyan] |[/] [cyan bold]v{version}[/]"
click.rich_click.ERRORS_SUGGESTION = f"[blue bold]TbLG[/] [cyan bold]v{version}[/]\nRun '[cyan]tblg --help or -h[/]' to show help message."
click.rich_click.STYLE_ERRORS_SUGGESTION = "cyan italic"
click.rich_click.STYLE_OPTION = "cyan"

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    "vcf_files",
    nargs=-1,
    required=True,
    type=click.Path(exists=True),
    metavar="[VCF FILES]",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Write results to file [dim]['.txt', '.tsv', or '.csv']",
)
@click.version_option(version, "-v", "--version", is_flag=True)
@click.pass_context
def main(ctx, vcf_files, output):
    """
    Process one or more VCF files and genotype lineages.
    """
    validator = InputOutputValidator(ctx, vcf_files, output)
    validator.validate_input()
    validator.validate_output()

    results_list = process_vcf_files(vcf_files)

    if not results_list:
        rprint("[red bold]ATTENTION[/]: [italic]No valid VCF files were found!")
        return

    results = combine_results(results_list)

    if output:
        write_results_to_file(results, output)
    else:
        print_results(results)


if __name__ == "__main__":
    sys.exit(main())
