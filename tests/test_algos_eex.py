__author__ = "Warren"

from unittest import TestCase

import pandas as pd
from zipline.finance import trading
from zipline.utils.factory import create_simulation_parameters
from zipline.test_algorithms import TestAlgorithm
from zipline.finance.commission import PerShare

from gg.powerline.utils.data.data_generator import DataGeneratorEex
from gg.powerline.exchanges.eex_exchange import EexExchange


class TestEexAlgo(TestCase):
    """
    Tests the change in pnl and position for a simple EEX weekly algo.
    """
    @classmethod
    def setUp(cls):
        exchange = EexExchange()
        trading.environment = exchange.env
        trading.environment.update_asset_finder(
            asset_finder=exchange.asset_finder)
        source = exchange.source()
        ident = source.identifiers[3]
        sid = trading.environment.asset_finder.retrieve_asset_by_identifier(
            ident).sid
        sim_params = create_simulation_parameters(start=source.start,
                                                  end=source.end)

        cls.algo = TestAlgorithm(sid=sid, amount=1, order_count=1,
                                  instant_fill=True,
                                  asset_finder=exchange.asset_finder,
                                  sim_params=sim_params,
                                  commission=PerShare(0))

        cls.data, cls.pnl = DataGeneratorEex(identifier=ident).create_data()
        cls.results = cls.algo.run(cls.data)

    def test_algo_pnl(self):
        for dt, pnl in self.pnl.iterrows():
            self.assertEqual(self.results.pnl[dt], pnl[0])

    def test_algo_positions(self):
        expected_positions = pd.DataFrame([0, 1, 1, 0], index=self.pnl.index)
        for dt, amount in expected_positions.iterrows():
            if self.results.positions[dt]:
                actual_position = self.results.positions[dt][0]['amount']
            else:
                actual_position = 0

            self.assertEqual(actual_position, amount[0])

    @classmethod
    def tearDownClass(cls):
        cls.algo = None
        trading.environment = None
