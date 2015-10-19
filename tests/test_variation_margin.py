from unittest import TestCase
import pandas as pd
from zipline.finance import trading
from zipline.utils.factory import create_simulation_parameters
from zipline.finance.commission import PerShare
from zipline.finance.slippage import FixedSlippage
from gg.powerline.utils.data.data_generator import DataGeneratorEex
from gg.powerline.exchanges.eex_exchange import EexExchange
from gg.powerline.test_algorithms import FlippingAlgorithm
from gg.powerline.finance.performance import variation_margin_and_costs


__author__ = 'Stefan Hackmann'


class TestVariationMargin(TestCase):
    """
    Tests the change in pnl and position for a simple EEX weekly algo.
    """
    @classmethod
    def setUpClass(cls):
        start = pd.Timestamp('2014-05-18',
                             tz='Europe/Berlin').tz_convert('UTC')
        end = pd.Timestamp('2015-05-22',
                           tz='Europe/Berlin').tz_convert('UTC')
        exchange = EexExchange(start=start, end=end)

        env = exchange.env
        env.write_data(futures_data=exchange.asset_metadata)

        ident = '2013-05-20_F1B4'
        sid = env.asset_finder.lookup_future_symbol(ident).sid

        instant_fill = True

        cls.data, cls.pnl, cls.expected_positions = DataGeneratorEex(
            identifier=ident,
            env=env,
            instant_fill=instant_fill).create_flipping()

        sim_params = create_simulation_parameters(
            start=cls.data.start,
            end=cls.data.end)

        cls.algo = FlippingAlgorithm(
            sid=sid, amount=1, commission=PerShare(0),
            slippage=FixedSlippage(0), env=env, sim_params=sim_params,
            instant_fill=instant_fill, data_frequency="minute")

        cls.results = cls.algo.run(cls.data)

    def test_algo_pnl(self):
        margin, costs = variation_margin_and_costs(self.results)
        algo_pnl = margin + costs
        for dt, pnl in self.pnl.iterrows():
            self.assertEqual(algo_pnl[dt], pnl[0])

    def test_algo_positions(self):
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
