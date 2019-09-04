import unittest
import pandas as pd

from benchutils.metrics import l2_norm, auprc


class TestMetrics(unittest.TestCase):

    def test_l2_norm_basic(self):
        input_ = pd.Series([1, 0])
        output = pd.Series([0, 0])
        expected = 1
        observed = l2_norm(input_, output)
        self.assertAlmostEqual(observed, expected)

    def test_auprc_basic(self):
        exp_profile = pd.Series([0.5, 0.4, 0.1, 0])
        obs_profile = pd.Series([0.4, 0.3, 0.05, 0.25])
        # calculate area under pr curve by hand
        expected_auprc = (1 / 3) * (2 / 3) + 0.5 * (1 / 3) * \
                         (0.75 - (2 / 3)) + (2 / 3)
        observed_auprc = auprc(obs_profile, exp_profile)
        self.assertAlmostEqual(observed_auprc, expected_auprc)
