from unittest import TestCase
import pandas as pd
from zipline.finance import trading
from zipline.utils.factory import create_simulation_parameters
from zipline.finance.commission import PerShare
from zipline.finance.slippage import FixedSlippage
from gg.powerline.utils.data.data_generator import DataGeneratorEex
from gg.powerline.exchanges.eex_exchange import EexExchange
from gg.powerline.test_algorithms import FlippingAlgorithm
from gg.powerline.finance.performance import pnl_and_costs


__author__ = 'Stefan Hackmann'


class TestPnl(TestCase):
    """
    Tests the change in pnl and position for a simple EEX weekly algo.
    """
    @classmethod
    def setUpClass(cls):
        start = pd.Timestamp('2014-05-18',
                             tz='Europe/Berlin').tz_convert('UTC')
        end = pd.Timestamp('2014-05-22',
                           tz='Europe/Berlin').tz_convert('UTC')
        products = ['F1B1', 'F1B2', 'F1B3', 'F1B4', 'F1B5']
        exchange = EexExchange(start=start, end=end, products=products)

        env = exchange.env
        env.write_data(futures_data=exchange.asset_metadata)

        sid = 0
        ident = env.asset_finder.retrieve_asset(sid).symbol

        instant_fill = True
        commission = 0.01

        cls.data, cls.pnl, cls.expected_positions = DataGeneratorEex(
            identifier=ident,
            env=env,
            instant_fill=instant_fill).create_flipping(168, commission)

        sim_params = create_simulation_parameters(
            start=cls.data.start,
            end=cls.data.end)

        cls.algo = FlippingAlgorithm(
            sid=sid, amount=1, commission=PerShare(commission),
            slippage=FixedSlippage(0), env=env, sim_params=sim_params,
            instant_fill=instant_fill, data_frequency="minute")

        cls.results = cls.algo.run(cls.data)

    def test_pnl(self):
        # TODO get rid of fix and use new zipline master, see below
        pnl, costs = pnl_and_costs(self.results, 168)
        algo_pnl = pnl - costs
        for dt, expected_pnl in self.pnl.iterrows():
            # self.assertAlmostEqual(self.results.pnl[dt], expected_pnl[0])
            self.assertEqual(algo_pnl[dt], expected_pnl[0])

    def test_positions(self):
        for dt, amount in self.expected_positions.iterrows():
            if self.results.positions[dt]:
                actual_position = \
                    self.results.positions[dt][0]['amount']
            else:
                actual_position = 0
            self.assertEqual(actual_position, amount[0])

    @classmethod
    def tearDownClass(cls):
        cls.algo = None
        trading.environment = None
