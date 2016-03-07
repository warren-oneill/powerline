from unittest import TestCase
import pandas as pd
from zipline.finance import trading
from zipline.utils.factory import create_simulation_parameters
from zipline.test_algorithms import TestAlgorithm
from zipline.finance.commission import PerShare
from zipline.finance.slippage import FixedSlippage
from gg.powerline.utils.data.data_generator import DataGeneratorEex
from gg.powerline.exchanges.eex_exchange import EexExchange


__author__ = "Warren"


class TestEexAlgoTrue(TestCase):
    """
    Tests the change in pnl and position for a simple EEX weekly algo.
    """
    @classmethod
    def setUpClass(cls):
        start = pd.Timestamp('2015-05-18', tz='Europe/Berlin').tz_convert(
            'UTC')
        end = pd.Timestamp('2015-05-22', tz='Europe/Berlin').tz_convert('UTC')
        exchange = EexExchange(start=start, end=end)

        env = exchange.env
        # TODO: create metadata manually here
        day = '2015-05-20'
        ident = exchange.insert_ident(day, exchange.products[0])
        expiration_date = pd.Timestamp(day,
                                       tz='Europe/Berlin').tz_convert('UTC')
        asset_metadata = {0: {
                'asset_type': 'future', 'symbol': ident,
                'expiration_date': expiration_date, 'contract_multiplier': 168,
                'end_date': expiration_date}}
        env.write_data(futures_data=asset_metadata)

        instant_fill = True

        cls.data, cls.pnl, cls.expected_positions = DataGeneratorEex(
            identifier=ident,
            env=env,
            instant_fill=instant_fill).create_simple()

        sim_params = create_simulation_parameters(
            start=cls.data.start,
            end=cls.data.end)

        cls.algo = TestAlgorithm(sid=0, amount=1, order_count=1,
                                 instant_fill=instant_fill,
                                 env=env,
                                 sim_params=sim_params,
                                 commission=PerShare(0),
                                 slippage=FixedSlippage())

        cls.results = cls.algo.run(cls.data)

    def test_algo_pnl(self):
        for dt, pnl in self.pnl.iterrows():
            self.assertEqual(self.results.pnl[dt], pnl[0])

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


class TestEexAlgoFalse(TestCase):
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
        day = '2015-05-20'
        ident = exchange.insert_ident(day, exchange.products[0])
        expiration_date = pd.Timestamp(day,
                                       tz='Europe/Berlin').tz_convert('UTC')
        asset_metadata = {0: {
                'asset_type': 'future', 'symbol': ident,
                'expiration_date': expiration_date, 'contract_multiplier': 168,
                'end_date': expiration_date}}
        env.write_data(futures_data=asset_metadata)

        instant_fill = False

        cls.data, cls.pnl, cls.expected_positions = DataGeneratorEex(
            identifier=ident,
            env=env,
            instant_fill=instant_fill).create_simple()

        sim_params = create_simulation_parameters(
            start=cls.data.start,
            end=cls.data.end)

        cls.algo = TestAlgorithm(sid=0, amount=1, order_count=1,
                                 instant_fill=instant_fill,
                                 env=env,
                                 sim_params=sim_params,
                                 commission=PerShare(0),
                                 slippage=FixedSlippage())

        cls.results = cls.algo.run(cls.data)

    def test_algo_pnl(self):
        for dt, pnl in self.pnl.iterrows():
            self.assertEqual(self.results.pnl[dt], pnl[0])

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
