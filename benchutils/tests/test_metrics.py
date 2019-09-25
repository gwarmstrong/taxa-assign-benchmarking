import unittest
import numpy as np

from benchutils.metrics import (precision, recall, f1, l1_norm, l2_norm, auprc,
                                pearsonr, rmse)


class TestMetrics(unittest.TestCase):

    def test_precision_basic(self):
        exp_profile = pd.Series([0.3, 0.4, 0.1, 0.2, 0])
        obs_profile = pd.Series([0.3, 0, 0.2, 0.2, 0.1])
        # calculate precision by hand
        expected = ((exp_profile > 0) & (obs_profile > 0)).sum() / \
                   (obs_profile > 0).sum()
        observed = precision(obs_profile, exp_profile)
        self.assertAlmostEqual(observed, expected)

    def test_recall_basic(self):
        exp_profile = pd.Series([0.3, 0.4, 0.1, 0.2, 0])
        obs_profile = pd.Series([0.3, 0, 0.2, 0, 0.5])
        # calculate recall by hand
        expected = ((exp_profile > 0) & (obs_profile > 0)).sum() / \
                   (exp_profile > 0).sum()
        observed = recall(obs_profile, exp_profile)
        self.assertAlmostEqual(observed, expected)

    def test_f1_basic(self):
        exp_profile = pd.Series([0, 0.4, 0, 0.1, 0.5])
        obs_profile = pd.Series([0.3, 0.2, 0, 0.2, 0.1])
        # calculate F1 score by hand
        expected = ((exp_profile > 0) & (obs_profile > 0)).sum() * 2 / \
                   ((exp_profile > 0).sum() + (obs_profile > 0).sum())
        observed = f1(obs_profile, exp_profile)
        self.assertAlmostEqual(observed, expected)

    def test_auprc_basic(self):
        exp_profile = np.array([0.5, 0.4, 0.1, 0])
        obs_profile = np.array([0.4, 0.3, 0.05, 0.25])
        # calculate area under pr curve by hand
        expected_auprc = (1 / 3) * (2 / 3) + 0.5 * (1 / 3) * \
                         (0.75 - (2 / 3)) + (2 / 3)
        observed_auprc = auprc(obs_profile, exp_profile)
        self.assertAlmostEqual(observed_auprc, expected_auprc)

    def test_pearsonr_basic(self):
        exp_profile_orig = np.array([0.5, 0.4, 0.1, 0])
        obs_profile = np.array([0.4, 0.3, 0.05, 0.25])

        exp_profile = np.array(exp_profile_orig)

        numerator = ((exp_profile - exp_profile.mean()) *
                     (obs_profile - obs_profile.mean())).sum()
        denominator_sq = ((exp_profile - exp_profile.mean()) ** 2).sum() * \
                         ((obs_profile - obs_profile.mean()) ** 2).sum()

        denominator = np.sqrt(denominator_sq)
        expected_pearsonr = numerator / denominator
        observed_pearsonr = pearsonr(obs_profile, exp_profile_orig)
        self.assertAlmostEqual(observed_pearsonr, expected_pearsonr)

    def test_l1_norm_basic(self):
        input_ = pd.Series([0, 0.1, 0.3, 0.1, 0.5])
        output = pd.Series([0.2, 0, 0, 0.4, 0.4])
        # calculate L1 norm by hand
        expected = np.sum(np.absolute(input_ - output))
        observed = l1_norm(input_, output)
        self.assertAlmostEqual(observed, expected)

    def test_l2_norm_basic(self):

        input_ = np.array([1, 0])
        output = np.array([0, 0])
        expected = 1
        observed = l2_norm(input_, output)
        self.assertAlmostEqual(observed, expected)

        input_ = np.array([0.2, 0.3, 0.4, 0, 0.1])
        output = np.array([0, 0.6, 0, 0.3, 0.1])
        # calculate L2 norm by hand
        expected = np.sqrt(np.sum(np.square(input_ - output)))
        observed = l2_norm(input_, output)
        self.assertAlmostEqual(observed, expected)

    def test_rmse_basic(self):
        input_ = np.array([1, 0])
        output = np.array([0, 0])
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

    def test_runs_metric_pearsonr(self):
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
