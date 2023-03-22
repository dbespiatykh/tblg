"""Process levels.tsv file"""
from importlib.resources import files

import pandas as pd


def get_levels_data():
    """
    Read the data from a TSV file containing information about barcoding levels, and extract the relevant data
    for each level. The data for each level is then stored in a tuple of NumPy arrays, where each array
    contains the position, the reference allele, the alternative allele, and the lineage for each row in the data.
    Additionally, the function returns an array of positional data that is common to all levels.


    Returns:
    -------
    levels_data : Tuple[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], np.ndarray]
        A tuple of NumPy arrays, where each sub-tuple contains the data for a different level. Each sub-tuple
        contains four arrays representing the position, the reference allele, the alternative allele,
        and the lineage for each row in the data.
    pos : np.ndarray
        An array containing the position for all SNPs.
    """
    levels_file = files("tblg.data").joinpath("levels.tsv")
    temp_df = pd.read_csv(levels_file, sep="\t")
    unique_levels = temp_df["level"].unique()
    levels_dict = {}

    # For each unique level value, extract the relevant data and store it in the dictionary
    for elem in unique_levels:
        levels_dict[elem] = temp_df[temp_df["level"] == elem][
            ["POS", "REF", "ALT", "lineage"]
        ]

    # Create a tuple of NumPy arrays, where each array contains the data for a different level
    # Each array contains the positional data, the reference allele, the alternative allele,
    # and the lineage (i.e., the level value) for each row in the data
    # The tuple contains data for levels 1 through 5
    levels_data = tuple(
        levels_dict.get(i, pd.DataFrame())[["POS", "REF", "ALT", "lineage"]]
        .to_numpy()
        .T
        for i in range(1, 6)
    )

    pos = temp_df["POS"].values

    return levels_data, pos
