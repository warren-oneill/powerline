__author__ = "Warren"

from unittest import TestCase
from datetime import timedelta, datetime
from nose.tools import nottest
import pandas as pd

from zipline.finance import trading

from gg.powerline.utils import tradingcalendar_epex, tradingcalendar_eex
from gg.powerline.exchanges.eex_exchange import EexExchange
from gg.powerline.exchanges.epex_exchange import EpexExchange


# TODO not being tested properly
class TestTradingCalendarEex(TestCase):
    """
    Tests trading times and trading days for EEX calendar by comparing with
    the benchmark and the DataSource.
    """
    @classmethod
    def setUpClass(cls):
        cls.exchange = EexExchange()
        trading.environment = cls.exchange.env
        trading.environment.update_asset_finder(
            asset_metadata=cls.exchange.asset_metadata)

    def test_calendar_vs_environment_eex(self):
        cal_days = trading.environment.benchmark_returns[
            tradingcalendar_eex.start:].index
        bounds = trading.environment.trading_days.slice_locs(
            start=tradingcalendar_eex.start,
            end=cal_days[-1]
            )

        env_days = trading.environment.trading_days[bounds[0]:bounds[1]]
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

    def test_calendar_vs_databank_eex(self):
        start = pd.Timestamp(datetime(day=10, month=10, year=2014), tz='UTC')
        end = pd.Timestamp(datetime(day=17, month=10, year=2014), tz='UTC')
        source = self.exchange.source(start=start, end=end)

        cal_days = trading.environment.benchmark_returns[
            source.start:source.end].index
        row = next(source)
        for expected_dt in cal_days:
            self.assertEqual(expected_dt, row.dt)

            while expected_dt == row.dt and row.dt < source.end:
                row = next(source)

    @classmethod
    def tearDownClass(cls):
        trading.environment = None


class TestTradingCalendarEpex(TestCase):
    """
    Tests trading times and trading days for EPEX calendar by comparing with
    the benchmark and the DataSource.
    """
    @classmethod
    def setUpClass(cls):
        cls.exchange = EpexExchange()
        trading.environment = cls.exchange.env
        # trading.environment.update_asset_finder(
        #    asset_metadata=cls.exchange.asset_metadata)

    def test_calendar_vs_environment_epex(self):
        cal_days = trading.environment.benchmark_returns[tradingcalendar_epex.start:]\
            .index
        bounds = trading.environment.trading_days.slice_locs(
            start=tradingcalendar_epex.start,
            end=cal_days[-1]
            )

        env_days = trading.environment.trading_days[bounds[0]:bounds[1]]
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

    # TODO do this test differently. shouldn't be testing db
    @nottest
    def test_calendar_vs_databank_epex(self):
        start = pd.Timestamp(datetime(day=10, month=10, year=2014), tz='UTC')
        end = pd.Timestamp(datetime(day=17, month=10, year=2014), tz='UTC')
        source = self.exchange.source(start=start, end=end)
        products = [str(i).zfill(2) + '-' + str(i+1).zfill(2) for i in
                    range(0, 24)]
        cal_days = trading.environment.benchmark_returns[
            source.start:source.end-timedelta(days=1)].index
        # TODO insert missing data in database
        for expected_dt in cal_days:
            if str(expected_dt.date()) == '2014-01-30' or \
                    str(expected_dt.date()) == '2014-04-15':
                continue
            for product in products:
                # Summer time
                if (str(expected_dt.date()) == '2014-03-29' or
                        str(expected_dt.date()) == '2015-03-28') and product \
                        == '02-03':
                    continue
                # Winter time
                if (str(expected_dt.date()) == '2014-10-25' or
                        str(expected_dt.date()) == '2015-10-24') and product\
                        == '03-04':
                    row = next(source)
                    self.assertEqual('02-03b', row.product, expected_dt.date())
                    self.assertEqual(expected_dt.date(), row.dt.date())

                row = next(source)
                self.assertEqual(product, row.product, expected_dt.date())
                self.assertEqual(expected_dt.date(), row.dt.date(),
                                 row.product)

    @classmethod
    def tearDownClass(cls):
        trading.environment = None
