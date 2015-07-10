__author__ = 'Warren'

from unittest import TestCase
import multiprocessing as mp
import numpy as np
from threading import Thread
from time import sleep

from zipline.finance import trading
from zipline.utils.factory import create_simulation_parameters
from zipline.finance.commission import PerShare

from gg.powerline.test_algorithms import TestEpexMessagingAlgorithm
from gg.powerline.exchanges.epex_exchange import EpexExchange
from gg.powerline.utils.data.data_generator import DataGeneratorEpex
from gg.messaging.json_consumer import JsonConsumer
from gg.messaging.exchange import Exchange

class TestEpexAlgo(TestCase):
    """
    Tests the change in pnl and position for a simple hourly EPEX algo.
    """
    def setUp(self):
        self.consumer = JsonConsumer()
        thread = Thread(target=self.consumer.run)
        thread.daemon = True
        thread.start()

        exchange = EpexExchange()
        trading.environment = exchange.env
        trading.environment.update_asset_finder(
            asset_finder=exchange.asset_finder)
        source = exchange.source()

        ident = source.identifiers[3]
        self.day = trading.environment.asset_finder.\
            retrieve_asset_by_identifier(ident).expiration_date
        sid = trading.environment.asset_finder.retrieve_asset_by_identifier(
            ident).sid
        sim_params = create_simulation_parameters(start=source.start,
                                                  end=source.end)
        amounts = np.full(24, 1)  # order 1MW for every hour
        self.algo = TestEpexMessagingAlgorithm(
            sid=sid, amount=amounts, order_count=1, instant_fill=False,
            asset_finder=exchange.asset_finder, sim_params=sim_params,
            commission=PerShare(0), data_frequency='minute', day=self.day
        )

        self.data, self.pnl = DataGeneratorEpex(identifier=ident).create_data()
        self.results = self.run_algo()

    def run_algo(self):
        results = self.algo.run(self.data)
        sleep(150)
        #self.algo.producer.close()
        return results

    def test_algo_pnl(self):
        for dt, pnl in self.pnl.iterrows():
            self.assertEqual(1, 2, self.consumer.data)
