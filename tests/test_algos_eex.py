from unittest import TestCase

from powerline.utils.data.data_generator import DataGeneratorEex
from powerline.exchanges.exchange import EexExchange as exchange
from powerline.utils.algos.eex_algo import initialize, handle_data

from zipline.finance import trading
from zipline.algorithm import TradingAlgorithm

from datetime import timedelta


class TestEexAlgo(TestCase):

    def setUp(self):
        trading.environment = exchange.env
        trading.environment.update_asset_finder(
            asset_finder=exchange.asset_finder)

        self.algo = TradingAlgorithm(initialize=initialize,
                                     handle_data=handle_data,
                                     asset_finder=exchange.asset_finder,
                                     sim_params=exchange.sim_params,
                                     instant_fill=True)
        self.data, self.pnl = DataGeneratorEex().create_data()

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
