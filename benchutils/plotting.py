import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def _metric_getter(x): return x.split('.')[-2]


def _method_stripper(x): return '_'.join(x.split('_')[1:])


def _load_summary_series(df_loc):
    df = pd.read_csv(df_loc, sep='\t',
                     names=['method', _metric_getter(df_loc)])
    df['method'] = df['method'].map(_method_stripper)
    return df


def metrics_scatterplot(metrics_df, x_offset=None, scatterplot_kwargs=None):
    """makes a scatterplot of the first column in `metrics_df` by the
    second column in `metrics_df`

    Parameters
    ----------
    metrics_df : pd.DataFrame
        DataFrame containing numerical measurments in the first two columns
    x_offset : float
        amount to offset scatterplot point labels by
    scatterplot_kwargs : dict
        kwargs to be passed to sns.scatterplot


    Returns
    -------
    matplotlib.figure.Figure
        figure containing the scatterplot
    matplotlib.axes.Axes
        the axes of the scatterplot

    """
    # TODO maybe refactor to take two series/arrays (sklearn-like)
    if scatterplot_kwargs is None:
        scatterplot_kwargs = dict()
    fig, ax = plt.subplots(figsize=(4, 4))
    x_name = metrics_df.columns[0]
    y_name = metrics_df.columns[1]
    sns.scatterplot(data=metrics_df, x=x_name, y=y_name, ax=ax,
                    **scatterplot_kwargs)
    x_min, x_max = ax.get_xlim()
    if x_offset is None:
        # TODO should be some other sanity check here
        x_offset = (x_max - x_min) / 50
    for index, row in metrics_df.T.iteritems():
        ax.text(row[x_name] + x_offset, row[y_name], index)
    return fig, ax


def methods_swarmplot(measurements, swarmplot_kwargs=None):
    # TODO can probably refactor the columns to be a little more general,
    #  e.g., sns.swarmplot(x=method_column, y=measurements_column, ...),
    #  where these variables are passed in
    """Makes a swarmplot of the values in the second column of
    `measurements` by the value in their `method` column (presumably the
    first column).

    Parameters
    ----------
    measurements : pd.DataFrame
        a DataFrame containing two columns, the first being title 'method',
        and the second containing floats
    swarmplot_kwargs
        kwargs to be passed to sns.swarmplot

    Returns
    -------
    matplotlib.figure.Figure
        figure containing the swarmplot
    matplotlib.axes.Axes
        the axes of the swarmplot

    """
    if swarmplot_kwargs is None:
        swarmplot_kwargs = dict()
    fig, ax = plt.subplots(figsize=(4, 4))
    y_name = measurements.columns[1]
    sns.swarmplot(x='method', y=y_name, data=measurements, ax=ax,
                  **swarmplot_kwargs)

    return fig, ax


def metric_comparison_plot(metric1_file, metric2_file, output_file,
                           scatterplot_kwargs=None):
    """Makes a scatterplot for each tuple in zip(files_metric1,
    files_metric2) that have the same entries in each. First metric is
    x-axis and second metric is y-axis.

    Parameters
    ----------
    metric1_file : str
        filepath to the series to be used for the x-axis of the scatterplot
    metric2_file : str
        filepath to the series to be used for the y-axis of the scatterplot
    output_file : str
        name of the output file
    scatterplot_kwargs : dict
        kwargs to be passed to sns.scatterplot

    """
    # TODO WARN and drop if there is an index in one file not in the other
    if scatterplot_kwargs is None:
        scatterplot_kwargs = dict()
    df1 = _load_summary_series(metric1_file)
    df2 = _load_summary_series(metric2_file)
    df1.set_index('method', inplace=True)
    df2.set_index('method', inplace=True)
    df = pd.concat([df1, df2], axis=1)
    fig, _ = metrics_scatterplot(df, scatterplot_kwargs=scatterplot_kwargs)
    fig.savefig(output_file, bbox_inches='tight')


def method_comparison_plot(list_of_files, output_file,
                           swarmplot_kwargs=None):
    """Makes a swarmplot, where each row in a file adds an entry to
    a corresponding box/category in the plot.

    Parameters
    ----------
    list_of_files : list of str
        list of paths to all files that should be concatenated for the
        swarmplot
    output_file : str
        name of the output file
    swarmplot_kwargs : dict
        kwargs to be passed to sns.swarmplot

    """
    if swarmplot_kwargs is None:
        swarmplot_kwargs = dict()
    # TODO sanity check files
    # LOAD list_of_files
    dfs = [_load_summary_series(df_) for df_ in list_of_files]

    # make plot containing all df's concatenated together
    measurements = pd.concat(dfs)
    measurements['Method'] = ['_'.join(method.split('_')[:-1]) for method in
                              measurements['method'].values]

    swarmplot_kwargs.update({'hue': 'Method'})
    fig, ax = methods_swarmplot(measurements,
                                swarmplot_kwargs=swarmplot_kwargs)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # write out plot (as svg)
    fig.savefig(output_file, bbox_inches='tight')
