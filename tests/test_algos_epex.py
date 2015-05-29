from unittest import TestCase
from nose.tools import nottest

from powerline.utils.algos.epex_algo import initialize, handle_data, ident
from powerline.exchanges.exchange import EpexExchange as exchange
from powerline.utils.data.data_generator import DataGeneratorEpex

from zipline.finance import trading
from zipline.algorithm import TradingAlgorithm


class TestEpexAlgo(TestCase):

    def setUp(self):
        trading.environment = exchange.env
        trading.environment.update_asset_finder(
            asset_finder=exchange.asset_finder)
        exchange.data_source()

        self.algo = TradingAlgorithm(initialize=initialize,
                                     handle_data=handle_data,
                                     asset_finder=exchange.asset_finder,
                                     sim_params=exchange.sim_params,
                                     instant_fill=True)
        self.data, self.pnl = DataGeneratorEpex(identifier=ident).create_data()

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
