import unittest
import pandas as pd

from benchutils.metrics import l2_norm


class TestMetrics(unittest.TestCase):

    def test_l2_norm_basic(self):
        input_ = pd.Series([1, 0])
        output = pd.Series([0, 0])
        expected = 1
        observed = l2_norm(input_, output)
        self.assertAlmostEqual(observed, expected)
