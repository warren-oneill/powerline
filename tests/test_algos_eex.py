from unittest import TestCase

from powerline.utils.algos.eex_algo import algo as algo_eex
from powerline.utils.data.data_generator import DataGeneratorEex

from zipline.finance import trading

from datetime import timedelta


class TestEexAlgo(TestCase):

    def setUp(self):
        self.algo = algo_eex
        self.data, self.pnl = DataGeneratorEex().create_data()

    def run_algo(self):
        print(trading.environment.bm_symbol)
        results = self.algo.run(self.data)
        return results

    def test_algo(self):
        results_algo = self.run_algo()

        for dt, pnl in self.pnl.iterrows():
            # pnl timestamps are at market close
            dt += timedelta(hours=17)

            self.assertEqual(results_algo.pnl[dt], pnl[0])

    def tearDown(self):
        self.algo = None
        trading.environment = None
