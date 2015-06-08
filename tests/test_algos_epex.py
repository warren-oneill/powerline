from unittest import TestCase
import pandas as pd
from nose.tools import nottest

from powerline.utils.algos.epex_algo import initialize, handle_data, ident
from powerline.exchanges.epex_exchange import EpexExchange
from powerline.utils.data.data_generator import DataGeneratorEpex

from zipline.finance import trading
from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import create_simulation_parameters


class TestEpexAlgo(TestCase):

    def setUp(self):
        exchange = EpexExchange()
        trading.environment = exchange.env
        trading.environment.update_asset_finder(
            asset_finder=exchange.asset_finder)
        source = exchange.source()
        sim_params = create_simulation_parameters(start=source.start,
                                                  end=source.end)

        self.algo = TradingAlgorithm(initialize=initialize,
                                     handle_data=handle_data,
                                     asset_finder=exchange.asset_finder,
                                     sim_params=sim_params,
                                     instant_fill=True)
        self.data, self.pnl = DataGeneratorEpex(identifier=ident).create_data()
        self.results = self.run_algo()

    def run_algo(self):
        results = self.algo.run(self.data)
        return results

    # @nottest
    def test_algo_pnl(self):
        for dt, pnl in self.pnl.iterrows():
            # pnl timestamps are at market close
            self.assertEqual(self.results.pnl[dt], pnl[0])

    def test_algo_positions(self):
        expected_positions = pd.DataFrame([1, 1, 0, 0, 0],
                                          index=self.pnl.index)
        for dt, amount in expected_positions.iterrows():
            if self.results.positions[dt]:
                actual_position = self.results.positions[dt][0]['amount']
            else:
                actual_position = 0

            self.assertEqual(actual_position, amount[0])

    def tearDown(self):
        self.algo = None
        trading.environment = None
