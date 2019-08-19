import os
from numpy.linalg import norm


def absolute_error(observed_file, expected_file, rank):
    pass


def correlation(observed_file, expected_file, rank):
    pass


def l2_loss(observed_file, expected_file, rank):
    # load dataframes
    # align the profiles for the sample
    # then calculate the l2_loss based on the aligned profiles
    # then output an error for the file
    # write out in some standardized format
    # TODO maybe need to think about the high level structure
    pass


def auprc(observed_file, expected_file, rank):
    pass

# TODO can probably make into one metrics function that loads the
#  dataframes, then put in a call to a specific `method`


def load_observed_profile(observed_file, method):
    # hope to not need method category
    pass


def load_expected_profile(expected_file):
    pass


def write_results(results, output_file):
    pass


available_metrics = {'correlation': correlation,
                     'l2_loss': l2_loss,
                     'auprc': auprc,
                     'absolute_error': absolute_error}


# TODO could make more sense to try to avoid ballooning files at this step,
#  and profile a batch of samples together
def profile_error(observed_file, expected_file, output_file, rank, metric,
                  method='kraken2'):
    load_observed_profile(observed_file, method=method)
    load_expected_profile(expected_file)

    if metric in available_metrics:
        results = available_metrics[metric](observed_file, expected_file, rank)
    else:
        raise ValueError('Metric \'{}\' is not in available metrics.')

    # TODO can delete the touch if real writing has been written
    os.system('touch {}'.format(output_file))
    write_results(results, output_file)
