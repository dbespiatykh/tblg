<img align ="left" src=./assets/logo.svg width=250px style="padding-right: 25px; padding-top: 25px;">

# A command-line tool to genotype _Mycobacterium tuberculosis_ lineage from a VCF file

## Description

The Tuberculosis Lineage Genotyping (TbLG) is a tool that uses variant call format `VCF` files to quickly and accurately assign a lineage to isolates of the _Mycobacterium tuberculosis_ complex (MTBC).

## Installation

```bash
pip install tblg
```

Alternatively:

1. Clone **TbLG** repository:

```bash
git clone https://github.com/dbespiatykh/tblg.git
```

2. Install TbLG

```bash
pip install .
```

3. Run TbLG:

```bash
stblg -h
```

## Usage

```bash
Usage: tblg [OPTIONS] <vcf_files>

  TbLG (Tuberculosis Lineage Genotyping)

  Process one or more VCF files and genotype lineages.

  VCF_FILES: One or more VCF files to be processed.

Options:
  -o, --output PATH  Write results to file '.txt', '.tsv', or '.csv'.
  -h, --help         Show this message and exit.
```

- Note: If an asterisk `*` appears in a 1 or 2 level lineage call, it indicates that the lineage contains only one of two barcoding SNPs.
