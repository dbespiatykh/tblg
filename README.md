<img align ="left" src=https://github.com/dbespiatykh/tblg/raw/main/assets/logo.svg width=250px style="padding-right: 25px; padding-top: 25px;">

# A command-line tool to genotype _Mycobacterium tuberculosis_ lineage from a VCF file

[![PyPI version](https://badge.fury.io/py/tblg.svg)](https://badge.fury.io/py/tblg)

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

- By default, the output is written to the standard output (stdout) in tabular format. However, the user can use the option `-o` or `--output` to change the output format to either a tab-separated or comma-separated file.

```bash
+----+-------------+-----------+----------------+-----------+------------+-----------+
|    | Sample      | Level 1   | Level 2        | Level 3   | Level 4    | Level 5   |
+====+=============+===========+================+===========+============+===========+
|  0 | SRR16370211 | L2        | L2.2 (ancient) | 2.2.1.2   |            |           |
+----+-------------+-----------+----------------+-----------+------------+-----------+
|  1 | SRR13180266 | L3        | L3.4           |           |            |           |
+----+-------------+-----------+----------------+-----------+------------+-----------+
|  2 | SRR12395111 | L4        | L2.2 (ancient) | L2.2.AA1  |            |           |
+----+-------------+-----------+----------------+-----------+------------+-----------+
|  3 | SRR13180370 | L4        | L4.1           | L4.1.4    |            |           |
+----+-------------+-----------+----------------+-----------+------------+-----------+
|  4 | SRR13180364 | L4        | L4.3           | L4.3.1    |            |           |
+----+-------------+-----------+----------------+-----------+------------+-----------+
|  5 | ERR1203060  | L5        | L5.1           | L5.1.2    |            |           |
+----+-------------+-----------+----------------+-----------+------------+-----------+
|  6 | ERR552796   | M.bovis   |                |           |            |           |
+----+-------------+-----------+----------------+-----------+------------+-----------+
```

- Note: If an asterisk `*` appears in a 1 or 2 level lineage call, it indicates that the lineage contains only one of two barcoding SNPs.

```bash
+----+-------------+-----------+----------------+-----------+------------+-----------+
|    | Sample      | Level 1   | Level 2        | Level 3   | Level 4    | Level 5   |
+====+=============+===========+================+===========+============+===========+
|  1 | sample_1    | L2        | L2.2 (ancient) | L2.2.AA3  | L2.2.AA3.1 |           |
+----+-------------+-----------+----------------+-----------+------------+-----------+
|  2 | sample_2    | L2*       | L2.1*          |           |            |           |
+----+-------------+-----------+----------------+-----------+------------+-----------+
```
