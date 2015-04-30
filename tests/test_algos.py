from unittest import TestCase

from powerline.utils.algos.phelix_algo import algo
from powerline.exchanges.exchange import EexExchange
from powerline.utils.data.data_generator import DataGenerator

from zipline.finance import trading

import pandas as pd
from datetime import timedelta


class TestEexAlgo(TestCase):
    _multiprocess_shared_ = True

    def setUp(self):
        self.algo = algo
        self.data, df = DataGenerator(EexExchange).create_data()
        prices = df.values
        self.pnl = pd.DataFrame([0, (prices[1][0]-prices[0][0])*168,
                                (prices[2][0]-prices[1][0])*168, 0],
                                index=df.index)

    def run_algo(self):
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
