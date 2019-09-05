import unittest
import pandas as pd
import numpy as np

from benchutils.metrics import l2_norm, auprc, correlation, rmse


class TestMetrics(unittest.TestCase):

    def test_auprc_basic(self):
        exp_profile = pd.Series([0.5, 0.4, 0.1, 0])
        obs_profile = pd.Series([0.4, 0.3, 0.05, 0.25])
        # calculate area under pr curve by hand
        expected_auprc = (1 / 3) * (2 / 3) + 0.5 * (1 / 3) * \
                         (0.75 - (2 / 3)) + (2 / 3)
        observed_auprc = auprc(obs_profile, exp_profile)
        self.assertAlmostEqual(observed_auprc, expected_auprc)

    def test_correlation_basic(self):
        exp_profile = pd.Series([0.5, 0.4, 0.1, 0])
        obs_profile = pd.Series([0.4, 0.3, 0.05, 0.25])

        numerator = ((exp_profile - exp_profile.mean()) *
                     (obs_profile - obs_profile.mean())).sum()
        denominator_sq = ((exp_profile - exp_profile.mean()) ** 2).sum() * \
                         ((obs_profile - obs_profile.mean()) ** 2).sum()

        denominator = np.sqrt(denominator_sq)
        expected_correlation = numerator / denominator
        observed_correlation = correlation(obs_profile, exp_profile)
        self.assertAlmostEqual(observed_correlation, expected_correlation)

    def test_l2_norm_basic(self):
        input_ = pd.Series([1, 0])
        output = pd.Series([0, 0])
        expected = 1
        observed = l2_norm(input_, output)
        self.assertAlmostEqual(observed, expected)

    def test_rmse_basic(self):
        input_ = pd.Series([1, 0])
        output = pd.Series([0, 0])
        expected = np.sqrt(1 / 2)
        observed = rmse(input_, output)
        self.assertAlmostEqual(observed, expected)


# TODO test these (blocked by unittest filesystem)
class TestProfileError(unittest.TestCase):

    def test_errors_metric_not_in_available_metrics(self):
        pass

    def test_errors_rank_not_in_ranks(self):
        pass

    def test_runs_metric_auprc(self):
        pass

    def test_runs_metric_correlation(self):
        pass

    def test_runs_metric_rmse(self):
        pass

    def test_runs_metric_l2_norm(self):
        pass

    def test_runs_with_list(self):
        pass

    def test_runs_with_string(self):
        pass


if __name__ == '__main__':
    unittest.main()
