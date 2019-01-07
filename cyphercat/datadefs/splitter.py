from torch import randperm
from torch._utils import _accumulate
#from torch.utils.data import Dataset, ConcatDataset
from torch.utils.data.dataset import Subset
#from torch.utils.data import Subset, random_split

import numpy as np
import pandas as pd


def dataset_split(dataset=None, lengths=None, indices=None):
    """
    Split a dataset into non-overlapping new datasets of given lengths.
    If indices is undefined, then a random permutation of dataset
    is generated. Slight modification of torch.utils.data.random_split
    to gain access to permuted indices.

    Arguments:
        dataset (Dataset): Dataset to be split
        lengths (sequence): lengths of splits to be produced
        indices (tensor): permutations of instances

    Returns:
        indices (tensor): premutations of instances

    """
    if sum(lengths) != len(dataset):
        raise ValueError("Sum of input lengths does not equal the length of the input dataset!")

    # If requested a random split of dataset
    if indices is None:
        indices = randperm(sum(lengths))

    #print((indices).int().numpy())
    #raw_input("TEST")
    #indices = (indices).int().numpy()
    indices = (indices).long()

    return indices, [Subset(dataset, indices[offset - length:offset]) for offset, length in zip(_accumulate(lengths), lengths)]


def splitter(dfs={}, df=None, unique_categories=[], category_id='', splits=[], N=-1):
    """ Splits the data for given unqie categories according to specified fractions.
    
    Args:
        dfs (dict(Dataframe): Current dictionary of dataframes. New splits
            will be concatenated to this dict.
        df (Dataframe): Dataframe containg all of the data and metadata.
        unique_categories (list(int)): List containing the indices of categories
            to include in these splits.
        category_id (string): Defining category for dataset in Dataframe object.
        splits (list(float)): List containing the fraction of the data to be
            included in each split.
        N (int): index to assign new splits when appending to dfs.

    Returns:
        (dict(Dataframe)): Updated dictionary of data splits.

    Example:
    
    Todo:
        - Add example.
    """
    # N is to keep track of the dataframe dict keys
    n_splits = len(splits)
    for category in unique_categories: # for each category

        # category = valid_sequence.unique_categories[0]
        tot_files = sum(df[category_id] == category)

        mini_df = df[df[category_id] == category]    
        mini_df = mini_df.reset_index()

        used_files = 0
        start_file = 0
        for idx, s in enumerate(splits): # for each split
            if idx != n_splits-1:
                n_files = int(s*tot_files)
                used_files += n_files
            else:
                n_files = tot_files - used_files

            # get stop index for the desired # of files:
            stop_file = start_file + n_files

            # initialize if first category, or append if later category
            if category == unique_categories[0]:
                dfs[idx + N] = (mini_df.iloc[start_file:stop_file])
            else:
                dfs[idx + N] = dfs[idx + N].append(mini_df.iloc[start_file:
                                                                stop_file])