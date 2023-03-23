"""
TbLG (Tuberculosis Lineage Genotyping)

A command-line tool to genotype Mycobacterium tuberculosis lineage from a VCF file

Author: Dmitry Bespiatykh
"""
import codecs
import os.path
import sys

import click

from .barcoding import process_vcf_files
from .utils import combine_results, print_results, write_results_to_file


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


version = get_version("__init__.py")

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version, "-v", "--version", is_flag=True)
@click.argument(
    "vcf_files", nargs=-1, type=click.Path(exists=True), metavar="<vcf_files>"
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Write results to file '.txt', '.tsv', or '.csv'.",
)
@click.pass_context
def main(ctx, vcf_files, output):
    """
    TbLG (Tuberculosis Lineage Genotyping).

    Process one or more VCF files and genotype lineages.

    VCF_FILES: One or more VCF files to be processed.
    """
    if not vcf_files and not ctx.params.get("help"):
        click.echo("Note: Please provide one or more VCF files to process\n")
        click.echo(ctx.get_help())
        ctx.exit()

    if output:
        if not output.endswith((".txt", ".tsv", ".csv")):
            raise SystemExit("Output file must have extension 'txt', 'tsv', or 'csv'")
        else:
            click.echo(f"Writing results to {output}")

    results_list = process_vcf_files(vcf_files)

    if not results_list:
        print("No valid VCF files were found!")

    results = combine_results(results_list)

    if output:
        write_results_to_file(results, output)
    else:
        print_results(results)


if __name__ == "__main__":
    sys.exit(main())
