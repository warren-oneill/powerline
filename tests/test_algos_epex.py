from unittest import TestCase

from powerline.utils.algos.epex_algo import algo as algo_epex
from powerline.utils.data.data_generator import DataGeneratorEpex
from powerline.assets.epex_metadata import MetadataFromSql
from powerline.utils import tradingcalendar_epex as calendar
from powerline.data.loader_power import load_market_data as load

from zipline.finance import trading
from zipline.finance.trading import TradingEnvironment


class TestEpexAlgo(TestCase):

    def setUp(self):

        self.algo = algo_epex
        self.data, self.pnl = DataGeneratorEpex().create_data()

    def run_algo(self):
        print(trading.environment.bm_symbol)
        results = self.algo.run(self.data)
        return results

    def test_algo(self):
        results_algo = self.run_algo()

        for dt, pnl in self.pnl.iterrows():
            # pnl timestamps are at market close

            self.assertEqual(results_algo.pnl[dt], pnl[0])

    def tearDown(self):
        self.algo = None
        trading.environment = None
