"""
TbLG (Tuberculosis Lineage Genotyping)

A command-line tool to genotype Mycobacterium tuberculosis lineage from a VCF file

Author: Dmitry Bespiatykh
"""
import sys

import click

from .barcoding import process_vcf_files
from .utils import (
    InputOutputValidator,
    combine_results,
    get_version,
    print_results,
    write_results_to_file,
)

version = get_version("__init__.py")

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    "vcf_files", nargs=-1, type=click.Path(exists=True), metavar="<vcf_files>"
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Write results to file '.txt', '.tsv', or '.csv'.",
)
@click.version_option(version, "-v", "--version", is_flag=True)
@click.pass_context
def main(ctx, vcf_files, output):
    """
    TbLG (Tuberculosis Lineage Genotyping).

    Process one or more VCF files and genotype lineages.

    VCF_FILES: One or more VCF files to be processed.
    """
    validator = InputOutputValidator(ctx, vcf_files, output)
    validator.validate_input()
    validator.validate_output()

    results_list = process_vcf_files(vcf_files)

    if not results_list:
        click.secho("ATTENTION: No valid VCF files were found!", bold=True)
        return

    results = combine_results(results_list)

    if output:
        write_results_to_file(results, output)
    else:
        print_results(results)


if __name__ == "__main__":
    sys.exit(main())
