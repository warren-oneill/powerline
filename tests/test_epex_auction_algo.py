import json
from unittest import TestCase
from datetime import timedelta

import pandas as pd
import numpy as np
from nose.tools import nottest
from zipline.utils.factory import create_simulation_parameters
from zipline.finance.commission import PerShare

from powerline.test_algorithms import TestAuctionAlgorithm
from powerline.exchanges.epex_exchange import EpexExchange
from powerline.utils.data.data_generator import DataGeneratorEpex
from powerline.finance.auction import auction

__author__ = "Warren"
# TODO close positions in intraday


class TestEpexAlgo(TestCase):
    """
    Tests the change in pnl and position for a simple hourly EPEX algo.
    """
    @classmethod
    def setUpClass(cls):
        start = pd.Timestamp('2014-01-03', tz='Europe/Berlin').tz_convert(
            'UTC')
        end = pd.Timestamp('2015-01-07', tz='Europe/Berlin').tz_convert('UTC')
        exchange = EpexExchange(start=start, end=end)

        env = exchange.env
        ident = '2015-06-01_01-02'
        day = '2015-06-01'
        expiration_date = pd.Timestamp('2015-06-01 00:30',
                                       tz='Europe/Berlin').tz_convert('UTC')

        # TODO: create metadata manually here
        # TODO: add each hour in day to metadata
        asset_metadata = {}
        for i, product in enumerate(exchange.products['hour']):
            ident = exchange.insert_ident(day, product)
            asset_metadata.update({i: {
                'asset_type': 'future', 'symbol': ident,
                'expiration_date': expiration_date, 'contract_multiplier': 1,
                'children':
                    json.dumps(['CHILD1', 'CHILD2', 'CHILD3', 'CHILD4']),
                'end_date': expiration_date}})

        asset_metadata.update({i + 1: {
            'asset_type': 'future', 'symbol': 'CHILD1', 'expiration_date':
                expiration_date, 'end_date': expiration_date +
                timedelta(minutes=30),
                'contract_multiplier': 0.25},
            i + 2: {
                'asset_type': 'future', 'symbol': 'CHILD2', 'expiration_date':
                expiration_date + timedelta(minutes=15),
                'end_date': expiration_date + timedelta(minutes=45),
                'contract_multiplier': 0.25},
            i + 3: {
                'asset_type': 'future', 'symbol': 'CHILD3', 'expiration_date':
                expiration_date + timedelta(minutes=30),
                'end_date': expiration_date + timedelta(minutes=60),
                'contract_multiplier': 0.25},
            i + 4: {
                'asset_type': 'future', 'symbol': 'CHILD4', 'expiration_date':
                expiration_date + timedelta(minutes=45),
                'end_date': expiration_date + timedelta(minutes=75),
                'contract_multiplier': 0.25}})

        env.write_data(futures_data=asset_metadata)

        cls.day = env.asset_finder.\
            lookup_future_symbol(ident).expiration_date
        sid = env.asset_finder.lookup_future_symbol(
            ident).sid
        data_gen = DataGeneratorEpex(identifier=ident, env=env)
        cls.sid_children = data_gen.sid_qh
        cls.data, cls.pnl = data_gen.create_data()

        sim_params = create_simulation_parameters(start=cls.data.start,
                                                  end=cls.data.end)
        amounts = np.full(25, 1)  # order 1MW for every hour
        cls.algo = TestAuctionAlgorithm(
            sid=sid, amount=amounts, order_count=1, instant_fill=False,
            env=env, sim_params=sim_params,
            commission=PerShare(0), data_frequency='minute', day=cls.day,
            auction=auction)

        cls.results = cls.algo.run(cls.data)

    def test_algo_pnl(self):
        for dt, pnl in self.pnl.iterrows():
            self.assertEqual(self.results.pnl[dt], pnl[0], self.results.pnl)

    def test_algo_positions(self):
        expected_positions = pd.DataFrame([[1, 1, 1, 1], [1, 1, 1, 1],
                                           ],
                                          index=self.pnl.index)
        for dt, amounts in expected_positions.iterrows():
            for i, amount in enumerate(amounts):
                if self.results.positions[dt]:
                    actual_position = self.results.positions[dt][i]['amount']
                    sid = self.results.positions[dt][i]['sid']
                else:
                    actual_position = 0

            self.assertEqual(actual_position, amount)
            self.assertIn(sid, self.sid_children)

    @nottest
    def test_prognosis_api(self):
        ident = '2015-01-05_01Q1'
        asset = self.algo.trading_environment.asset_finder\
            .lookup_future_symbol(ident)

        start_dt = asset.end_date - timedelta(hours=2)
        algo_dts = pd.date_range(start_dt, freq='15min', periods=4)

        expected_values = np.array([435.9, 439.4, 445.8, 451.3])
        for i, amount in enumerate(expected_values):
            self.assertEqual(amount, self.algo.prognosis(asset.end_date,
                                                         algo_dts[i]))

    @classmethod
    def tearDownClass(cls):
        cls.algo = None
