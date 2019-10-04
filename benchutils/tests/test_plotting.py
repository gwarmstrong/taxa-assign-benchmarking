import unittest
from benchutils.tests import testbase
from benchutils import plotting


# TODO test errors (blocked by checking errors in plotting.py)
class TestMetricComparisonPlot(testbase.BaseTestCase):
    def test_runs_metric_comparison_plot(self):
        abs_error_file = self.get_data_path('summaries/2019.08.07_10.20.59_'
                                            'sample_0.genus.absolute_error'
                                            '.txt')
        corr_file = self.get_data_path('summaries/2019.08.07_10.20.59_sample_0'
                                       '.genus.correlation.txt')

        test_metric_plot = self.create_data_path(
            'summaries/test_metric_plot.svg')

        plotting.metric_comparison_plot(abs_error_file, corr_file,
                                        test_metric_plot)


# TODO test errors (blocked by checking errors in plotting.py)
class TestMethodComparisonPlot(testbase.BaseTestCase):
    def test_runs_method_comparison_plot(self):
        sample1 = self.get_data_path(
            'summaries/2019.08.07_10.20.59_sample_0.genus.correlation.txt')
        sample2 = self.get_data_path(
            'summaries/2019.08.07_10.20.59_sample_1.genus.correlation.txt')
        plot = self.create_data_path('summaries/test_method_plot.svg')
        plotting.method_comparison_plot([sample1, sample2], plot)


if __name__ == '__main__':
    unittest.main()
