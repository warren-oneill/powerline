__author__ = 'Warren'

from unittest import TestCase
from nose.tools import nottest
import numpy as np
from threading import Thread
from collections import OrderedDict
import pandas as pd
from datetime import timedelta
import time

from zipline.finance import trading
from zipline.utils.factory import create_simulation_parameters
from zipline.finance.commission import PerShare

from gg.powerline.test_algorithms import TestEpexMessagingAlgorithm
from gg.powerline.exchanges.epex_exchange import EpexExchange
from gg.powerline.utils.data.data_generator import DataGeneratorEpex
from gg.messaging.json_consumer import JsonConsumer


class TestMessanger(TestCase):
    """
    Tests the change in pnl sent by the messenger
    """
    def setUp(self):
        self.consumer = JsonConsumer()
        self.process = Thread(target=self.consumer.run)
        self.process.daemon = True
        self.process.start()

        products = {'hour': {'2015-06-01': '01-02'}}
        exchange = EpexExchange()
        trading.environment = exchange.env
        ident = '2015-06-01_01-02'
        expiration_date = pd.Timestamp('2015-06-01 00:30',
                                       tz='Europe/Berlin').tz_convert('UTC')
        asset_metadata = {ident: {
            'asset_type': 'future', 'symbol': ident, 'expiration_date':
            expiration_date, 'children': ['child1', 'child2', 'child3',
                                          'child4']},
            'child1': {
                'asset_type': 'future', 'symbol': 'child1', 'expiration_date':
                expiration_date, 'contract_multiplier': 0.25},
            'child2': {
                'asset_type': 'future', 'symbol': 'child2', 'expiration_date':
                expiration_date, 'contract_multiplier': 0.25},
            'child3': {
                'asset_type': 'future', 'symbol': 'child3', 'expiration_date':
                expiration_date, 'contract_multiplier': 0.25},
            'child4': {
                'asset_type': 'future', 'symbol': 'child4', 'expiration_date':
                expiration_date, 'contract_multiplier': 0.25}}

        trading.environment.update_asset_finder(
            asset_metadata=asset_metadata)

        self.data, self.pnl = DataGeneratorEpex(identifier=ident).create_data()
        sim_params = create_simulation_parameters(start=self.data.start,
                                                  end=self.data.end)

        amounts = np.full(25, 1)  # order 1MW for every hour
        self.algo = TestEpexMessagingAlgorithm(env=trading.environment,
            sid=0, amount=amounts, order_count=1, instant_fill=False,
            sim_params=sim_params,
            commission=PerShare(0), data_frequency='minute',
            day=expiration_date, products=products
        )

        self.results = self.run_algo()

    def run_algo(self):
        results = self.algo.run(self.data)
        return results

    @nottest
    def test_algo_pnl(self):
        time.sleep(10)
        data = OrderedDict(sorted(
        self.consumer.data.items(),
                                  key=lambda t: t[0]))
        expected_pnl = [0, 4, 9]
        for i, perf in enumerate(data.values()):
            self.assertEqual(expected_pnl[i], perf['pnl'])
