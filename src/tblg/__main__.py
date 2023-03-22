"""
TbLG (Tuberculosis Lineage Genotyping)

A command-line tool to genotype Mycobacterium tuberculosis lineage from a VCF file

Author: Dmitry Bespiatykh
"""
import sys

import click

from .barcoding import process_vcf_files
from .utils import combine_results, print_results, write_results_to_file

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
@click.pass_context
def main(ctx, vcf_files, output):
    """
    TbLG (Tuberculosis Lineage Genotyping)

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
