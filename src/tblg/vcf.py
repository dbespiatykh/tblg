"""Process VCF files"""
from gzip import open as gzopen

import numpy as np
import pandas as pd
from tqdm import tqdm

from .levels import get_levels_data


def validate_vcf(vcf_file):
    """
    Check if a VCF file has typical VCF structure.

    Returns True if the file has typical VCF structure, and False otherwise.
    """
    if vcf_file.endswith(".vcf.gz"):
        with gzopen(vcf_file, "rb") as f:
            for line in f:
                line = line.decode("utf-8")
                if line.startswith("#"):
                    continue
                else:
                    fields = line.strip().split("\t")
                    if len(fields) < 8:
                        tqdm.write(
                            f"{vcf_file} does not have typical VCF structure. Skipping..."
                        )
                        return False
                    else:
                        return True
    elif vcf_file.endswith(".vcf"):
        with open(vcf_file) as f:
            for line in f:
                if line.startswith("#"):
                    continue
                else:
                    fields = line.strip().split("\t")
                    if len(fields) < 8:
                        tqdm.write(
                            f"{vcf_file} does not have typical VCF structure. Skipping..."
                        )
                        return False
                    else:
                        return True
    else:
        tqdm.write(f"{vcf_file} does not end with .vcf or .vcf.gz. Skipping...")


def vcf_to_dataframe(file, use_tqdm=False):
    """
    Reads a VCF file and returns a Pandas DataFrame containing the sample names, position,
    and alternative allele for each sample in the VCF file.

    Parameters:
    ----------
    file : str
        The name of the VCF file to read. The file can be compressed with gzip.
    use_tqdm : bool, optional
        A flag that indicates whether or not to display a progress bar during the reading process.
        Default is False.

    Returns:
    -------
    df : pd.DataFrame
        A Pandas DataFrame containing the sample names, positional data, and allele data for each sample
        in the VCF file. The DataFrame is filtered to only include rows with positions that are present in
        the levels data extracted from the levels.tsv file.
    """
    pos_all = get_levels_data()[1]

    opener = gzopen if file.endswith(".gz") else open

    with opener(file, "rt") as f:
        # Remove all header lines from the input file
        lines = [line.strip() for line in f if not line.startswith("##")]

    # Extract the sample names from the first header line
    header = lines.pop(0).split("\t")[9:]

    # Extract data from each line of the input file and convert it to a list
    data = []

    if use_tqdm:
        pbar = tqdm(total=len(lines), desc="Reading VCF files", colour="blue")
    for i, line in enumerate(lines):
        fields = line.split("\t")
        pos, ref, alt = fields[1], fields[3], fields[4]
        alleles = [ref] + alt.split(",")
        genotypes = [genotype.split(":") for genotype in fields[9:]]

        for i, gt in enumerate(genotypes):
            if gt[0] == "." or gt[0] == "./." or gt[0] == ".|.":
                allele = np.nan
            elif "/" in gt[0]:
                alleles_list = [
                    alleles[int(x)] if x != "." else np.nan for x in gt[0].split("/")
                ]
                allele = "/".join([x for x in alleles_list if str(x) != "nan"])
            elif "|" in gt[0]:
                alleles_list = [
                    alleles[int(x)] if x != "." else np.nan for x in gt[0].split("|")
                ]
                allele = "|".join([x for x in alleles_list if str(x) != "nan"])
            else:
                allele = alleles[int(gt[0])]
            data.append([header[i], pos, ref, allele])
        if use_tqdm:
            pbar.update(1)
    if use_tqdm:
        pbar.close()

    # Convert the list of data to a Pandas DataFrame
    df = pd.DataFrame(data, columns=["Sample", "POS", "REF", "ALT"])

    # Set the data types for each column in the DataFrame
    df = df.astype(
        {"Sample": "object", "REF": "object", "ALT": "object", "POS": "int64"}
    )
    # Strip "/" and "|" from ALT column
    df["ALT"] = df["ALT"].str.split(r"[/|]").str[-1]

    # Filter the DataFrame to only include rows with positions in the pos_all list
    df = df[df["POS"].isin(pos_all)].reset_index(drop=True)
    # Return the filtered DataFrame
    return df
