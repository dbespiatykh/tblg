"""Barcoding related functions"""
import numpy as np
from tqdm.auto import tqdm

from .levels import get_levels_data
from .vcf import validate_vcf, vcf_to_dataframe


def lineage2_decision(call_list):
    """
    Determines the lineage 2 variant calls and returns a modified call list.

    Args:
    call_list (list): A list of variant calls.

    Returns:
    altList (list): A modified list of variant calls, where any call containing
                    both "L2.2 (modern)" and "L2.2 (ancient)" is modified to
                    contain only "L2.2 (modern)" and any call not containing
                    "L2.2 (modern)" is left unchanged.
    """
    lin2 = ["L2.2 (modern)", "L2.2 (ancient)"]
    alt_list = []
    for item in call_list:
        if all(i in item for i in lin2):
            item = list(set(item) - set(lin2))
            item.append(lin2[0])
        alt_list.append(item)
    return alt_list


def lineage4_decision(call_list, lin):
    """
    Determines the alternate alleles for lineage 4 based on the input call list and lineage 4 variants.
    This function takes a list of calls and a lineage as input and returns a new list
    that either removes the lineage if it exists in the call or adds the lineage to the
    call twice if it does not exist in the call.

    Args:
        call_list (List[List[str]]): A list of lists containing genotype calls for each sample at a given position.
        lin (List[str]): A list of lineage 4 variants.

    Returns:
        List[List[str]]: A list of lists containing the alternate alleles for each sample at a given position.
    """
    alt_list = []
    for item in call_list:
        if any(i in item for i in lin):
            item = [x for x in item if x not in lin]
        else:
            item.extend([lin[0] for i in range(2)])
        alt_list.append(item)
    return alt_list


def count_variants(call_list, prefix=None):
    """
    Count the number of occurrences of each variant in the input list and modify it as follows:
    - If a variant occurs more than once, keep it as-is.
    - If a variant occurs only once, concatenate it with a warning message in square brackets.
    - If a variant starts with the prefix string (if provided), remove it from the list.

    Args:
        call_list (List[str]): A list of variants.
        prefix (Optional[str]): A string prefix to remove from the list.

    Returns:
        List[str]: A modified version of the input list, with variants possibly concatenated with a warning message or removed.
    """
    d = {}
    for item in call_list:
        if item:
            caseless = item.casefold()
            if caseless in d:
                d[caseless][1] += 1
            else:
                d[caseless] = [item, 1]

    call_list = []
    for item, count in d.values():
        if not item.startswith(prefix) if prefix else True:
            item = f"{item}" if count > 1 else f"{item}*"
        call_list.append(item)

    return call_list


def barcoding(uploaded_vcf, use_tqdm=False):
    """
    Perform barcoding of a VCF file uploaded by the user.

    Parameters:
    -----------
    uploaded_vcf : str
        The file path or name of the uploaded VCF file.
    use_tqdm : bool, optional
        Whether or not to use tqdm to display progress bar (default is False).

    Returns:
    --------
    pandas.DataFrame
        A dataframe containing barcoding analysis results for each sample.
    """
    # Convert VCF to DataFrame
    df = vcf_to_dataframe(uploaded_vcf, use_tqdm=use_tqdm)

    # Get levels dictionary and create a list of level names
    levels = get_levels_data()[0]
    level_names = [f"level_{i+1}" for i in range(len(levels))]

    # Define a function to compute the level of each sample
    def compute_level(level):
        """
        The compute_level function takes a level tuple and computes the level for
        each sample in a DataFrame based on the values of "POS", "REF", and "ALT"
        columns of the DataFrame. It returns an array of levels for each sample.

        Parameters:
        -----------
        level: A tuple containing four elements
            - the position (POS), reference allele (REF), alternate allele (ALT)
            and the level number. This tuple represents a single level.
        Returns:
        --------
        levels: A numpy array containing the level number for each sample in the DataFrame.
        Note: This function assumes that the input DataFrame df has columns named "POS", "REF", and "ALT".
        """
        exp = (
            df["POS"].values[:, None],
            df["REF"].values[:, None],
            df["ALT"].values[:, None],
        )
        mask = np.logical_and.reduce(
            [
                np.equal(exp[0], level[0]),
                np.equal(exp[1], level[1]),
                np.equal(exp[2], level[2]),
            ]
        )
        return np.dot(mask, level[3])

    # Compute the level of each sample for each level
    for i, level in (
        enumerate(tqdm(levels, desc="Processing levels", colour="blue"))
        if use_tqdm
        else enumerate(levels)
    ):
        df[level_names[i]] = compute_level(level)

    # Drop the columns REF, ALT, and POS and replace empty strings with NaN
    df.drop(["REF", "ALT", "POS"], axis=1, inplace=True)
    df.replace("", np.nan, inplace=True)

    # Group the data by sample and concatenate the level columns into comma-separated strings
    df = df.groupby(["Sample"]).agg(lambda x: ",".join(x.dropna())).reset_index()

    # Split the first two level columns into lists and apply lineage decision and count variants functions
    df[level_names[:2]] = df[level_names[:2]].applymap(lambda x: x.split(","))
    df[level_names[0]] = lineage4_decision(df[level_names[0]], ["L4"])
    df[level_names[1]] = lineage4_decision(df[level_names[1]], ["L4.9"])
    df[level_names[0]] = df[level_names[0]].apply(count_variants, prefix="L8")
    df[level_names[1]] = df[level_names[1]].apply(
        count_variants, prefix=("L2.2 (modern)", "L2.2 (ancient)")
    )
    df[level_names[1]] = lineage2_decision(df[level_names[1]])

    # Convert the first two level columns back to comma-separated strings
    df[level_names[:2]] = df[level_names[:2]].applymap(lambda x: ", ".join(map(str, x)))

    # Sort the dataframe by level and reset the index
    df.sort_values(level_names, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Return the final dataframe
    return df


def process_vcf_files(vcf_files):
    """
    Process one or more VCF files and return a list of dataframes containing results
    """
    results_list = []

    # Check if only one VCF file is supplied
    if len(vcf_files) == 1:
        vcf_file = vcf_files[0]
        if validate_vcf(vcf_file):
            out = barcoding(vcf_file, use_tqdm=True)
            results_list.append(out)

    # If more than one VCF file is supplied, process each file and display a progress bar
    else:
        with tqdm(total=len(vcf_files), desc="Processing files", colour="blue") as pbar:
            for vcf_file in vcf_files:
                if validate_vcf(vcf_file):
                    out = barcoding(vcf_file, use_tqdm=False)
                    if (
                        out.empty
                        or all(
                            out.loc[:, out.columns != "Sample"]
                            .replace("", np.nan)
                            .isna()
                            .all()
                        )
                        is True
                    ):
                        tqdm.write(
                            f"{vcf_file} does not have any genotyping SNPs. Skipping..."
                        )
                    else:
                        results_list.append(out)
                pbar.update(1)

    return results_list
