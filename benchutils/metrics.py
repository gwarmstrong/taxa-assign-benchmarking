import pandas as pd
from benchutils import ranks
import numpy as np
from numpy.linalg import norm
from scipy.stats import pearsonr as scipy_pearsonr
from scipy.stats import spearmanr as scipy_spearmanr
from scipy.stats import entropy
from sklearn.metrics import (precision_score, recall_score, f1_score, auc,
                             precision_recall_curve)


def precision(observed, expected):
    """

    Parameters
    ----------
    observed : np.array, pd.Series
        The profile obtained by running a profiling method
    expected : np.array, pd.Series
        The ground truth relative abundance

    Returns
    -------
    float
        The precision score with > 0 positive, and negative otherwise

    """
    return precision_score((expected > 0).astype(float),
                           (observed > 0).astype(float))


def recall(observed, expected):
    """

    Parameters
    ----------
    observed : np.array, pd.Series
        The profile obtained by running a profiling method
    expected : np.array, pd.Series
        The ground truth relative abundance

    Returns
    -------
    float
        The recall score with > 0 positive, and negative otherwise

    """
    return recall_score((expected > 0).astype(float),
                        (observed > 0).astype(float))


def f1(observed, expected):
    """

    Parameters
    ----------
    observed : np.array, pd.Series
        The profile obtained by running a profiling method
    expected : np.array, pd.Series
        The ground truth relative abundance

    Returns
    -------
    float
        The F1 score with > 0 positive, and negative otherwise

    """
    return f1_score((expected > 0).astype(float),
                    (observed > 0).astype(float))


def rmse(observed, expected):
    """

    Parameters
    ----------
    observed : np.array
        The profile obtained by running a profiling method
    expected : np.array
        The ground truth relative abundance

    Returns
    -------
    float
        The root mean squared error between the series

    """
    # see https://stackoverflow.com/questions/21926020/how-to-calculate-rmse
    #  -using-ipython-numpy
    return np.sqrt(np.mean((observed - expected) ** 2))


def pearsonr(observed, expected):
    """

    Parameters
    ----------
    observed : np.array
        The profile obtained by running a profiling method
    expected : np.array
        The ground truth relative abundance

    Returns
    -------
    float
        The Pearson correlation between the series

    """
    return scipy_pearsonr(observed, expected)[0]


def spearmanr(observed, expected):
    """

    Parameters
    ----------
    observed : np.array
        The profile obtained by running a profiling method
    expected : np.array
        The ground truth relative abundance

    Returns
    -------
    float
        The Spearman correlation between the series

    """
    return scipy_spearmanr(observed, expected)[0]


def l1_norm(observed, expected):
    """

    Parameters
    ----------
    observed : np.array, pd.Series
        The profile obtained by running a profiling method
    expected : np.array, pd.Series
        The ground truth relative abundance

    Returns
    -------
    float
        The l1_norm between the series

    """
    return norm(observed - expected, ord=1)


def l2_norm(observed, expected):
    """

    Parameters
    ----------
    observed : np.array
        The profile obtained by running a profiling method
    expected : np.array
        The ground truth relative abundance

    Returns
    -------
    float
        The l2_norm between the series

    """
    return norm(observed - expected, ord=2)


def auprc(observed, expected):
    """

    Parameters
    ----------
    observed : np.array
        The profile obtained by running a profiling method
    expected : np.array
        The ground truth relative abundance

    Returns
    -------
    float
        The AUPRC with expected > 0 positive, and negative otherwise

    """
    expected = (expected > 0).astype(float)

    precision, recall, _ = precision_recall_curve(expected, observed)
    auprc_ = auc(recall, precision)
    return auprc_


def kl_divergence(observed, expected):
    """

    Parameters
    ----------
    observed : np.array
        The profile obtained by running a profiling method
    expected : np.array
        The ground truth relative abundance

    Returns
    -------
    float
        The Kullback-Leibler divergence from the observed distribution
        to the expected distribution

    """
    return entropy(expected, observed)


def _get_column_name(prefix, suffix):
    return prefix + '_' * (len(prefix) > 0) + 'PERCENTAGE_{}'.format(suffix)


def _load_df(file_, rank, suffix, prefix='', skiprows=0):
    # TODO docs
    # TODO have a "sniffer" to verify input format and throw error if
    #  input is incorrect
    df = pd.read_csv(file_, sep='\t', skiprows=skiprows)
    # TODO note that rank is chosen already by kraken
    df = df.loc[df['RANK'] == rank]
    df['@@TAXID'] = df['@@TAXID'].astype(int)
    df = df.set_index('@@TAXID')
    df = df[['PERCENTAGE']]
    percentage_name = _get_column_name(prefix, suffix)
    df = df.rename(columns={'PERCENTAGE': percentage_name})
    return df


def _load_observed_single_profile(observed_file, rank, suffix, prefix=''):
    # TODO docs
    df = _load_df(observed_file, rank, suffix, prefix=prefix)
    return df


def _load_observed_profiles(observed_files, rank, methods, prefix=''):
    # TODO docs
    # merge a bunch of dataframes loaded with `load_observed_single_profile
    dfs = []
    for observed_file, method in zip(observed_files, methods):
        dfs.append(_load_observed_single_profile(observed_file,
                                                 rank,
                                                 suffix=method,
                                                 prefix=prefix))
    return pd.concat(dfs, axis=1, sort=False)


def _load_expected_profile(expected_file, rank, prefix=''):
    # TODO docs
    df = _load_df(expected_file, rank, 'expected', prefix=prefix, skiprows=4)
    return df


# TODO unit test
def profile_error(observed_files, expected_file, output_file, rank,
                  methods, metric):
    """

    Parameters
    ----------
    observed_files : list of str or str
        A filepath to a profile returned by a method, or list of
        filepaths to profiles returned from a method
    expected_file : str
        A filepath to the ground truth profile
    output_file : str
        A filepath to write the results of the error profiling to
    rank : str
        A taxonomic rank to evaluate the error at
    methods : list of str or str
        Has the same shape as `observed_files` and details the method used
        in the corresponding observed file.
    metric : str
        A metric to use to evaluate the observed profiles

    Raises
    ------
    ValueError
        If `rank` is not an available/valid rank
        If `metric` is not an available/valid metric

    """

    if rank not in ranks:
        raise ValueError('Rank \'{}\' not in available ranks'.format(rank))

    if metric not in available_metrics:
        raise ValueError('Metric \'{}\' is not in available metrics.'.format(
            metric))

    if not isinstance(observed_files, list):
        observed_files = [str(observed_files)]
    else:
        observed_files = [str(file_) for file_ in observed_files]

    if isinstance(methods, str):
        methods = [methods]

    observed_profiles = _load_observed_profiles(observed_files, rank,
                                                methods)  # ,
    # prefix=expected_file)
    expected_profile = _load_expected_profile(expected_file, rank,
                                              )  # prefix=expected_file)

    # merges the dataframes to unify the indices in them, fills in missing
    # values with 0, then splits them back apart
    all_profiles = pd.concat([observed_profiles, expected_profile],
                             axis=1, sort=False, join='outer')
    # fill in na's and normalize to 1
    all_profiles = all_profiles.fillna(0) / 100
    observed_profiles = all_profiles.iloc[:, :-1]
    expected_profile = all_profiles.iloc[:, [-1]]
    # expected_profile = expected_profile.values.flatten()
    # TODO maybe take difference from sum to 100 as unassigned

    func = available_metrics[metric]
    results = [func(profile.values.flatten(),
                    expected_profile.values.flatten())
               for _, profile in observed_profiles.iteritems()]
    results = pd.Series(results, name=metric,
                        index=observed_profiles.columns)

    results.to_csv(output_file, sep='\t')


available_metrics = {'pearsonr': pearsonr,
                     'precision': precision,
                     'recall': recall,
                     'f1': f1,
                     'l1_norm': l1_norm,
                     'l2_norm': l2_norm,
                     'auprc': auprc,
                     'absolute_error': rmse,
                     'kl_divergence': kl_divergence,
                     'spearmanr': spearmanr}
