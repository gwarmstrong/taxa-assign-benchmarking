import unittest
from benchutils.tests import testbase
from benchutils.transformers import metaphlan2_transformer


class TestMetaphlan2Transformer(testbase.BaseTestCase):

    def test_metaphlan2_transformer_runs(self):
        profile = self.get_data_path('sample_metaphlan2_output.txt')
        output = self.create_data_path('metaphlan2_transformer_output.txt')
        metaphlan2_transformer(profile, [output], ranks=['genus'])


class TestKraken2Transformer(unittest.TestCase):
    # TODO (blocked by unittest filesystem)
    # TODO needs sample input
    pass


if __name__ == '__main__':
    unittest.main()
