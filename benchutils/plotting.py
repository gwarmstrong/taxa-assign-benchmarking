import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def absolute_error_plot(absolute_error_file, output_file):
    os.system('touch {}'.format(output_file))


def correlation_plot(correlation_file, output_file):
    os.system('touch {}'.format(output_file))


def metric_getter(x): return x.split('.')[-2]


def method_stripper(x): return '_'.join(x.split('_')[1:])


def _load_summary_series(df_loc):
    df = pd.read_csv(df_loc, sep='\t', names=['method', metric_getter(df_loc)])
    df['method'] = df['method'].map(method_stripper)
    df.set_index('method', inplace=True)
    return df


def metrics_scatterplot(df, x_offset=None, scatterplot_kwargs=None):
    if scatterplot_kwargs is None:
        scatterplot_kwargs = dict()
    fig, ax = plt.subplots(figsize=(4, 4))
    x_name = df.columns[0]
    y_name = df.columns[1]
    sns.scatterplot(data=df, x=x_name, y=y_name, ax=ax, **scatterplot_kwargs)
    x_min, x_max = ax.get_xlim()
    if x_offset is None:
        # TODO should be some other sanity check here
        x_offset = (x_max - x_min) / 50
    for index, row in df.T.iteritems():
        ax.text(row[x_name] + x_offset, row[y_name], index)
    return fig, ax


def metric_comparison_plot(metric1_file, metric2_file, output_file, *args,
                           **kwargs):
    """Makes a scatterplot for each tuple in zip(files_metric1,
    files_metric2) that have the same entries in each. First metric is
    x-axis and second metric is y-axis.

    Parameters
    ----------
    metric1_file
    metric2_file
    output_files

    Returns
    -------

    """
    # TODO WARN and drop if there is something in one file not in the other
    df1 = _load_summary_series(metric1_file)
    df2 = _load_summary_series(metric2_file)
    df = pd.concat([df1, df2], axis=1)
    fig, _ = metrics_scatterplot(df)
    fig.savefig(output_file, bbox_inches='tight')


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

