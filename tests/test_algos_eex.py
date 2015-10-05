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
    def setUpClass(cls):
        exchange = EexExchange()
        exchange.env.write_data(
            futures_data=exchange.asset_metadata)
        env = exchange.env

        ident = '2013-05-20_F1B4'
        sid = \
            env.asset_finder.lookup_future(ident).sid

        cls.data, cls.pnl = DataGeneratorEex(identifier=ident,
                                             env=env).create_data()

        sim_params = create_simulation_parameters(start=cls.data.start,
                                                  end=cls.data.end)

        cls.algo = TestAlgorithm(sid=sid, amount=1, order_count=1,
                                 instant_fill=True,
                                 env=env,
                                 sim_params=sim_params,
                                 commission=PerShare(0))

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
