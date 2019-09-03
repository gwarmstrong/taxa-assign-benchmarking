import unittest

from benchutils import plotting


class TestMetricComparisonPlot(unittest.TestCase):
    # TODO get filepaths for demo data and run it on them
    def test_metric_comparison_plot_runs(self):
        plotting.metric_comparison_plot('benchutils/tests/data/summaries/'
                                        '2019.08.07_10.20.59_sample_0.genus'
                                        '.absolute_error.txt',
                                        'benchutils/tests/data/summaries/'
                                        '2019.08.07_10.20.59_sample_0.genus'
                                        '.correlation.txt',
                                        'benchutils/tests/data/summaries/'
                                        'test_plot.svg')


class TestHelperFunctions(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
