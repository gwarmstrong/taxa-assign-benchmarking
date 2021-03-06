import unittest
import numpy as np
import pandas as pd

from benchutils.metrics import (precision, recall, f1, l1_norm, l2_norm, auprc,
                                pearsonr, spearmanr, rmse, profile_error)
from benchutils.tests import testbase


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

    def test_spearmanr_basic(self):
        exp_profile = np.array([1, 2, 3, 4, 5])
        obs_profile = np.array([5, 6, 7, 8, 7])
        observed_spearmanr = spearmanr(obs_profile, exp_profile)
        expected_spearmanr = 0.82078268166812329
        self.assertAlmostEqual(observed_spearmanr, expected_spearmanr)

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
class TestProfileError(testbase.BaseTestCase):

    def setUp(self):
        super(TestProfileError, self).setUp()
        self.exp = self.get_data_path('expected_genus_profile.txt')
        self.obs1 = self.get_data_path('sample_genus_profile1.txt')
        self.obs2 = self.get_data_path('sample_genus_profile2.txt')

    def test_errors_metric_not_in_available_metrics(self):
        with self.assertRaisesRegex(ValueError, 'not in available metrics'):
            profile_error('foo', 'bar', 'baz', rank='genus',
                          methods='qux', metric='quux')

    def test_errors_rank_not_in_ranks(self):
        with self.assertRaisesRegex(ValueError, 'not in available ranks'):
            profile_error('foo', 'bar', 'baz', rank='qux', methods='quux',
                          metric='f1')

    def test_runs_metric_auprc(self):
        out1 = self.create_data_path('test_runs_with_metric_auprc1.txt')
        out2 = self.create_data_path('test_runs_with_metric_auprc2.txt')
        profile_error(self.obs1, self.exp, out1, rank='genus',
                      methods='auprc', metric='auprc')
        profile_error([self.obs1, self.obs1], self.exp, out2, rank='genus',
                      methods=['auprc', 'auprc'], metric='auprc')

    def test_runs_metric_pearsonr(self):
        out1 = self.create_data_path('test_runs_with_metric_pearsonr1.txt')
        out2 = self.create_data_path('test_runs_with_metric_pearsonr2.txt')
        profile_error(self.obs1, self.exp, out1, rank='genus',
                      methods='pearsonr', metric='pearsonr')
        profile_error([self.obs1, self.obs1], self.exp, out2, rank='genus',
                      methods=['pearsonr', 'pearsonr'], metric='pearsonr')

    def test_runs_metric_spearmanr(self):
        out1 = self.create_data_path('test_runs_with_metric_spearmanr1.txt')
        out2 = self.create_data_path('test_runs_with_metric_spearmanr2.txt')
        profile_error(self.obs1, self.exp, out1, rank='genus',
                      methods='spearmanr', metric='spearmanr')
        profile_error([self.obs1, self.obs1], self.exp, out2, rank='genus',
                      methods=['spearmanr', 'spearmanr'], metric='spearmanr')

    def test_runs_metric_rmse(self):
        out1 = self.create_data_path('test_runs_with_metric_rmse1.txt')
        out2 = self.create_data_path('test_runs_with_metric_rmse2.txt')
        profile_error(self.obs1, self.exp, out1, rank='genus',
                      methods='absolute_error', metric='absolute_error')
        profile_error([self.obs1, self.obs1], self.exp, out2, rank='genus',
                      methods=['absolute_error', 'absolute_error'],
                      metric='absolute_error')

    def test_runs_metric_l1_norm(self):
        out1 = self.create_data_path('test_runs_with_metric_l1_norm1.txt')
        out2 = self.create_data_path('test_runs_with_metric_l1_norm2.txt')
        profile_error(self.obs1, self.exp, out1, rank='genus',
                      methods='l1_norm', metric='l1_norm')
        profile_error([self.obs1, self.obs1], self.exp, out2, rank='genus',
                      methods=['l1_norm', 'l1_norm'], metric='l1_norm')

    def test_runs_metric_l2_norm(self):
        out1 = self.create_data_path('test_runs_with_metric_l2_norm1.txt')
        out2 = self.create_data_path('test_runs_with_metric_l2_norm2.txt')
        profile_error(self.obs1, self.exp, out1, rank='genus',
                      methods='l2_norm', metric='l2_norm')
        profile_error([self.obs1, self.obs1], self.exp, out2, rank='genus',
                      methods=['l2_norm', 'l2_norm'], metric='l2_norm')

    def test_runs_metric_precision(self):
        out1 = self.create_data_path('test_runs_with_metric_precision1.txt')
        out2 = self.create_data_path('test_runs_with_metric_precision2.txt')
        profile_error(self.obs1, self.exp, out1, rank='genus',
                      methods='precision', metric='precision')
        profile_error([self.obs1, self.obs1], self.exp, out2, rank='genus',
                      methods=['precision', 'precision'], metric='precision')

    def test_runs_metric_recall(self):
        out1 = self.create_data_path('test_runs_with_metric_recall1.txt')
        out2 = self.create_data_path('test_runs_with_metric_recall2.txt')
        profile_error(self.obs1, self.exp, out1, rank='genus',
                      methods='recall', metric='recall')
        profile_error([self.obs1, self.obs1], self.exp, out2, rank='genus',
                      methods=['recall', 'recall'], metric='recall')


if __name__ == '__main__':
    unittest.main()
