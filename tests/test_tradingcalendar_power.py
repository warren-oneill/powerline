from zipline.finance.trading import TradingEnvironment
from zipline.finance import trading

from powerline.utils import tradingcalendar_eex
from powerline.utils import tradingcalendar_epex
from powerline.data.loader_power import load_market_data
from powerline.exchanges.exchange import EexExchange

from unittest import TestCase
from nose.tools import nottest

source_eex = EexExchange.source


class TestTradingCalendarEex(TestCase):
    def setUp(self):
        trading.environment = TradingEnvironment(
            bm_symbol='^EEX',
            exchange_tz='Europe/Berlin',
            env_trading_calendar=tradingcalendar_eex,
            load=load_market_data)
        self.env = trading.environment

    def test_calendar_vs_environment_eex(self):
        cal_days = self.env.benchmark_returns[tradingcalendar_eex.start:].index
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

    def test_calendar_vs_databank_eex(self):
        source = source_eex

        cal_days = self.env.benchmark_returns[source.start:source.end].index

        row = next(source)
        for expected_dt in cal_days:
            self.assertEqual(expected_dt, row.dt)

            dt_last = row.dt
            while dt_last == row.dt and row.dt != source.end:
                row = next(source)

    def tearDown(self):
        trading.environment = None


class TestTradingCalendarEpex(TestCase):
    def setUp(self):
        trading.environment = TradingEnvironment(
            bm_symbol='^EPEX',
            exchange_tz='Europe/Berlin',
            env_trading_calendar=tradingcalendar_epex,
            load=load_market_data)
        self.env = trading.environment

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

    @nottest
    def test_calendar_vs_databank_epex(self):
        source = 0  # TODO

        cal_days = self.env.benchmark_returns[source.start:source.end].index

        row = next(source)
        for expected_dt in cal_days:
            self.assertEqual(expected_dt, row.dt)

            dt_last = row.dt
            while dt_last == row.dt and row.dt != source.end:
                row = next(source)

    def tearDown(self):
        trading.environment = None
