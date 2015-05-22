from unittest import TestCase

from powerline.utils.algos.epex_algo import algo as algo_epex
from powerline.utils.data.data_generator import DataGeneratorEpex

from zipline.finance import trading

from nose.tools import nottest


class TestEpexAlgo(TestCase):
    def setUp(self):
        self.algo = algo_epex
        self.data, self.pnl = DataGeneratorEpex().create_data()

    def run_algo(self):
        results = self.algo.run(self.data)
        return results

    @nottest
    def test_algo(self):
        results_algo = self.run_algo()

        for dt, pnl in self.pnl.iterrows():
            # pnl timestamps are at market close

            self.assertEqual(results_algo.pnl[dt], pnl[0])

    def tearDown(self):
        self.algo = None
        trading.environment = None
