__author__ = 'Warren'

from unittest import TestCase
import numpy as np
from threading import Thread
import pandas as pd
import time

import json

from zipline.utils.factory import create_simulation_parameters
from zipline.finance.commission import PerShare

from gg.powerline.test_algorithms import TestEpexMessagingAlgorithm
from gg.powerline.exchanges.epex_exchange import EpexExchange
from gg.powerline.utils.data.data_generator import DataGeneratorEpex
from gg.messaging.json_consumer import JsonConsumer
from gg.powerline.finance.auction import auction


class TestMessanger(TestCase):
    """
    Tests the change in pnl sent by the messenger
    """

    def setUp(self):
        products = {'hour': {'2015-06-01': ['01-02']}}
        exchange = EpexExchange()
        env = exchange.env
        ident = '2015-06-01_01-02'
        expiration_date = pd.Timestamp('2015-06-01 00:30',
                                       tz='Europe/Berlin').tz_convert('UTC')
        asset_metadata = {0: {
            'asset_type': 'future', 'symbol': ident, 'expiration_date':
            expiration_date, 'children': json.dumps(['CHILD1', 'CHILD2',
                                                     'CHILD3', 'CHILD4']),
            'contract_multiplier': 1},
            1: {
                'asset_type': 'future', 'symbol': 'CHILD1', 'expiration_date':
                expiration_date, 'contract_multiplier': 0.25},
            2: {
                'asset_type': 'future', 'symbol': 'CHILD2', 'expiration_date':
                expiration_date, 'contract_multiplier': 0.25},
            3: {
                'asset_type': 'future', 'symbol': 'CHILD3', 'expiration_date':
                expiration_date, 'contract_multiplier': 0.25},
            4: {
                'asset_type': 'future', 'symbol': 'CHILD4', 'expiration_date':
                expiration_date, 'contract_multiplier': 0.25}}

        env.write_data(futures_data=asset_metadata)
        sid = env.asset_finder.lookup_future_symbol(ident).sid

        self.data, self.pnl = DataGeneratorEpex(identifier=ident, env=env
                                                ).create_data()
        sim_params = create_simulation_parameters(start=self.data.start,
                                                  end=self.data.end)

        amounts = np.full(25, 1)  # order 1MW for every hour
        self.algo = TestEpexMessagingAlgorithm(
            env=env, sid=sid, amount=amounts, order_count=1,
            instant_fill=False, sim_params=sim_params, commission=PerShare(0),
            data_frequency='minute', day=expiration_date, products=products,
            auction=auction
        )

        self.consumer = JsonConsumer()
        self.process = Thread(target=self.consumer.run)
        self.process.daemon = True
        self.process.start()

        self.results = self.run_algo()

    def run_algo(self):
        results = self.algo.run(self.data)
        return results

    def test_algo_pnl(self):
        time.sleep(10)
        data = self.consumer.data

        expected_pnl = 9
        self.assertEqual(expected_pnl, data['perf']['pnl'])
