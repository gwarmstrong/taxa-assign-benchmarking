import os
import pandas as pd
from benchutils import ranks


def absolute_error(observed_file, expected_file, output_file, rank):
    # TODO use rank to subset the expected true profile
    if rank not in ranks:
        raise ValueError('Rank \'{}\' not in available ranks'.format(rank))
    os.system('touch {}'.format(output_file))


def correlation(observed_file, expected_file, output_file, rank):
    if rank not in ranks:
        raise ValueError('Rank \'{}\' not in available ranks'.format(rank))
    os.system('touch {}'.format(output_file))
