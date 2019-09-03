import os


def absolute_error_plot(absolute_error_file, output_file):
    os.system('touch {}'.format(output_file))


def correlation_plot(correlation_file, output_file):
    os.system('touch {}'.format(output_file))


def metric_comparison_plot(files_metric1, files_metric2, output_file, *args,
                           **kwargs):
    """Makes a scatterplot for each tuple in zip(files_metric1,
    files_metric2) that have the same entries in each. First metric is
    x-axis and second metric is y-axis.

    Parameters
    ----------
    files_metric1
    files_metric2
    output_file

    Returns
    -------

    """
    # TODO WARN and drop if there is something in one file not in the other
    # TODO
    pass


def method_comparision_plot(list_of_files, output_file, *args, **kwargs):
    """Makes a boxplot/swarmplot, where each row in a file adds an entry to
    a corresponding box/category in the plot.

    Parameters
    ----------
    list_of_files
    output_file

    Returns
    -------

    """
    # TODO verify input
    # TODO LOAD list_of_files
    # TODO make plot containing all df's, separated by category (each series
    #  loaded should really be a row
    # TODO write out plot (as svg?)
    pass

