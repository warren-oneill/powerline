__author__ = 'Warren'

from unittest import TestCase
from nose.tools import nottest
import numpy as np
from threading import Thread
from collections import OrderedDict

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

        exchange = EpexExchange()
        trading.environment = exchange.env
        trading.environment.update_asset_finder(
            asset_finder=exchange.asset_finder)
        source = exchange.source()

        ident = trading.environment.asset_finder.cache[3].symbol
        self.day = trading.environment.asset_finder.\
            retrieve_asset_by_identifier(ident).expiration_date
        sid = trading.environment.asset_finder.retrieve_asset_by_identifier(
            ident).sid
        sim_params = create_simulation_parameters(start=source.start,
                                                  end=source.end)
        amounts = np.full(25, 1)  # order 1MW for every hour
        self.algo = TestEpexMessagingAlgorithm(
            sid=sid, amount=amounts, order_count=1, instant_fill=False,
            asset_finder=exchange.asset_finder, sim_params=sim_params,
            commission=PerShare(0), data_frequency='minute', day=self.day
        )

        self.data, self.pnl = DataGeneratorEpex(identifier=ident).create_data()
        self.results = self.run_algo()

    def run_algo(self):
        results = self.algo.run(self.data)
        return results

    @nottest
    def test_algo_pnl(self):
        data = OrderedDict(sorted(self.consumer.data.items(),
                                  key=lambda t: t[0]))
        expected_pnl = [0, 0, 4, 9]
        for i, pnl in enumerate(data.values()):
            self.assertEqual(expected_pnl[i], pnl)
