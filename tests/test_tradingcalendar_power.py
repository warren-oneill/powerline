from unittest import TestCase
from datetime import datetime

import pandas as pd

from powerline.utils import tradingcalendar_epex, tradingcalendar_eex
from powerline.exchanges.eex_exchange import EexExchange
from powerline.exchanges.epex_exchange import EpexExchange

__author__ = "Warren"


# TODO not being tested properly
class TestTradingCalendarEex(TestCase):
    """
    Tests trading times and trading days for EEX calendar by comparing with
    the benchmark and the DataSource.
    """
    @classmethod
    def setUpClass(cls):
        start = pd.Timestamp(datetime(day=10, month=10, year=2014), tz='UTC')
        end = pd.Timestamp(datetime(day=17, month=10, year=2014), tz='UTC')
        cls.exchange = EexExchange(start=start, end=end)
        cls.env = cls.exchange.env

    def test_calendar_vs_environment_eex(self):
        cal_days = self.env.benchmark_returns[
            tradingcalendar_eex.start:].index
        bounds = self.env.trading_days.slice_locs(
            start=tradingcalendar_eex.start,
            end=cal_days[-1]
        )

        env_days = self.env.trading_days[bounds[0]:bounds[1]]
        self.check_days(env_days, cal_days)

    def check_days(self, env_days, cal_days):
        diff = env_days - cal_days
        self.assertEqual(
            len(diff),
            0,
            "{diff} should be empty".format(diff=diff)
        )

        diff2 = cal_days - env_days
        self.assertEqual(
            len(diff2),
            0,
            "{diff} should be empty".format(diff=diff2)
        )

    @classmethod
    def tearDownClass(cls):
        pass


class TestTradingCalendarEpex(TestCase):
    """
    Tests trading times and trading days for EPEX calendar by comparing with
    the benchmark and the DataSource.
    """
    @classmethod
    def setUpClass(cls):
        start = pd.Timestamp(datetime(day=10, month=10, year=2014), tz='UTC')
        end = pd.Timestamp(datetime(day=17, month=10, year=2014), tz='UTC')
        cls.exchange = EpexExchange(start=start, end=end)
        cls.env = cls.exchange.env

    def test_calendar_vs_environment_epex(self):
        cal_days = self.env.benchmark_returns[tradingcalendar_epex.start:]\
            .index
        bounds = self.env.trading_days.slice_locs(
            start=tradingcalendar_epex.start,
            end=cal_days[-1]
        )

        env_days = self.env.trading_days[bounds[0]:bounds[1]]
        self.check_days(env_days, cal_days)

    def check_days(self, env_days, cal_days):
        diff = env_days - cal_days
        self.assertEqual(
            len(diff),
            0,
            "{diff} should be empty".format(diff=diff)
        )

        diff2 = cal_days - env_days
        self.assertEqual(
            len(diff2),
            0,
            "{diff} should be empty".format(diff=diff2)
        )

    @classmethod
    def tearDownClass(cls):
        pass
