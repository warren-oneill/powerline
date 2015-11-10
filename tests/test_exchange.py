__author__ = 'Warren'

from gg.powerline.exchanges.eex_exchange import EexExchange
from gg.powerline.exchanges.epex_exchange import EpexExchange
from gg.powerline.sources.eex_source import EexSource
from gg.powerline.sources.epex_source import EpexSource

from zipline.finance.commission import PerShare
from zipline.finance.trading import TradingEnvironment

import pandas as pd

from unittest import TestCase


# TODO add products test
class TestEexExchange(TestCase):

    def setUp(self):
        start = pd.Timestamp('2014-01-03', tz='Europe/Berlin').tz_convert(
            'UTC')
        end = pd.Timestamp('2014-01-07', tz='Europe/Berlin').tz_convert('UTC')
        self.exchange = EexExchange(start=start, end=end)

    def test_exchange(self):
        self.assertIsInstance(self.exchange.source, EexSource)
        self.assertIsInstance(self.exchange.commission, PerShare)

        benchmark, treasury_curve = self.loader()
        self.assertIsInstance(benchmark, pd.Series)
        self.assertIsInstance(treasury_curve, pd.DataFrame)
        self.assertIsInstance(self.exchange.asset_metadata, dict)
        self.assertIsInstance(self.exchange.calendar.trading_day,
                              pd.tseries.offsets.CDay)
        self.assertIsInstance(self.exchange.calendar.trading_days,
                              pd.DatetimeIndex)
        self.assertIsInstance(self.exchange.calendar.get_open_and_closes(
            self.exchange.calendar.trading_days, []), pd.DataFrame)
        self.assertIsInstance(self.exchange.env, TradingEnvironment)
        self.assertEqual(self.exchange.exchange_tz, 'Europe/Berlin')
        self.assertEqual(self.exchange.benchmark, '^EEX')

    def loader(self):
        return self.exchange.load(self.exchange.calendar.trading_day,
                                  self.exchange.calendar.trading_days,
                                  self.exchange.benchmark)

    def tearDown(self):
        self.exchange = []


class TestEpexExchange(TestCase):

    def setUp(self):
        start = pd.Timestamp('2014-01-03', tz='Europe/Berlin').tz_convert(
            'UTC')
        end = pd.Timestamp('2014-01-07', tz='Europe/Berlin').tz_convert('UTC')
        self.exchange = EpexExchange(start=start, end=end)

    def test_exchange(self):
        self.assertIsInstance(self.exchange.source, EpexSource)
        self.assertIsInstance(self.exchange.commission, PerShare)

        benchmark, treasury_curve = self.loader()
        self.assertIsInstance(benchmark, pd.Series)
        self.assertIsInstance(treasury_curve, pd.DataFrame)
        self.assertIsInstance(self.exchange.asset_metadata, dict)
        self.assertIsInstance(self.exchange.calendar.trading_day,
                              pd.tseries.offsets.CDay)
        self.assertIsInstance(self.exchange.calendar.trading_days,
                              pd.DatetimeIndex)
        self.assertIsInstance(self.exchange.calendar.get_open_and_closes(
            self.exchange.calendar.trading_days, []), pd.DataFrame)
        self.assertIsInstance(self.exchange.env, TradingEnvironment)
        self.assertEqual(self.exchange.exchange_tz, 'Europe/Berlin')
        self.assertEqual(self.exchange.benchmark, '^EPEX')

    def loader(self):
        return self.exchange.load(self.exchange.calendar.trading_day,
                                  self.exchange.calendar.trading_days,
                                  self.exchange.benchmark)

    def tearDown(self):
        self.exchange = []
