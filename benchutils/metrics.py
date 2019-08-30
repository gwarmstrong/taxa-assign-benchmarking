import os
import pandas as pd
from benchutils import ranks
import numpy as np
from numpy.linalg import norm
from scipy.stats import pearsonr
from itertools import combinations


def rmse(observed, expected):
    # see https://stackoverflow.com/questions/21926020/how-to-calculate-rmse
    #  -using-ipython-numpy
    predictions = observed.values.flatten()
    targets = expected.values.flatten()
    return np.sqrt(np.mean((predictions - targets) ** 2))


def correlation(observed, expected):
    return pearsonr(observed.values.flatten(),
                    expected.values.flatten())[0]


def l2_loss(observed, expected):
    return norm(observed.values.flatten() - expected.values.flatten(), ord=2)


def auprc(observed, expected):
    # TODO make actual function for calculating
    return pd.Series(np.zeros(len(observed.values.flatten())))


def get_column_name(prefix, suffix):
    return prefix + '_' * (len(prefix) > 0) + 'PERCENTAGE_{}'.format(suffix)


# TODO goal is to have a unified observed profile so that we can use the
#  same parser
def _load_df(file_, rank, suffix, prefix='', skiprows=0):
    df = pd.read_csv(file_, sep='\t', skiprows=skiprows)
    # TODO note that rank is chosen already by kraken
    df = df.loc[df['RANK'] == rank]
    df['@@TAXID'] = df['@@TAXID'].astype(int)
    df = df.set_index('@@TAXID')
    df = df[['PERCENTAGE']]
    percentage_name = get_column_name(prefix, suffix)
    df = df.rename(columns={'PERCENTAGE': percentage_name})
    return df


def load_observed_single_profile(observed_file, rank, suffix, prefix=''):
    df = _load_df(observed_file, rank, suffix, prefix=prefix)
    return df


def load_observed_profiles(observed_files, rank, methods, prefix=''):
    # merge a bunch of dataframes loaded with `load_observed_single_profile
    dfs = []
    for observed_file, method in combinations(observed_files, methods):
        dfs.append(load_observed_single_profile(observed_file,
                                                rank,
                                                suffix=method,
                                                prefix=prefix))
    return pd.concat(dfs, axis=1, sort=False)


def load_expected_profile(expected_file, rank, prefix=''):
    df = _load_df(expected_file, rank, 'expected', prefix=prefix, skiprows=4)
    return df


def write_results(results: pd.Series, output_file):
    results.to_csv(output_file, sep='\t')


def profile_error(observed_files, expected_file, output_file, rank,
                  methods, metric):

    if rank not in ranks:
        raise ValueError('Rank \'{}\' not in available ranks'.format(rank))

    if isinstance(observed_files, str):
        observed_files = [observed_files]

    if isinstance(methods, str):
        methods = [methods]

    observed_profiles = load_observed_profiles(observed_files, rank,
                                               methods)  # ,
    # prefix=expected_file)
    expected_profile = load_expected_profile(expected_file, rank,
                                             )  # prefix=expected_file)

    # merges the dataframes to unify the indices in them, fills in missing
    # values with 0, then splits them back apart
    all_profiles = pd.concat([observed_profiles, expected_profile],
                             axis=1, sort=False)
    # fill in na's and normalize to 1
    all_profiles = all_profiles.fillna(0) / 100
    observed_profiles = all_profiles.iloc[:, :-1]
    expected_profile = all_profiles.iloc[:, [-1]]
    # TODO maybe take difference from sum to 100 as unassigned

    # maybe map and add to a series
    if metric in available_metrics:
        func = available_metrics[metric]
        results = map(lambda x: func(observed_profiles[x], expected_profile),
                      observed_profiles.columns)
        # results = available_metrics[metric](observed_profiles,
        #                                     expected_profile)
        results = pd.Series(results, name=metric,
                            index=observed_profiles.columns)
    else:
        raise ValueError('Metric \'{}\' is not in available metrics.')

    write_results(results, output_file)


# each should return something like a dataframe
available_metrics = {'correlation': correlation,
                     'l2_loss': l2_loss,
                     'auprc': auprc,
                     'absolute_error': rmse}
