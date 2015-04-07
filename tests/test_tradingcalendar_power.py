from zipline.finance.trading import TradingEnvironment

from powerline.utils import tradingcalendar_eex as tradingcalendar_eex
from powerline.data.loader_power import load_market_data
from powerline.sources.eex_source import SqlSource

from unittest import TestCase


class TestTradingCalendarPower(TestCase):
    def setUp(self):
        self.env = TradingEnvironment(
            bm_symbol='^EEX',
            exchange_tz='Europe/Berlin',
            env_trading_calendar=tradingcalendar_eex,
            load=load_market_data)

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

    def test_calendar_vs_databank(self):
        source = SqlSource()

        cal_days = self.env.benchmark_returns[source.start:source.end].index

        row = next(source)
        for expected_dt in cal_days:
            self.assertEqual(expected_dt, row.dt)

            dt_last = row.dt
            while dt_last == row.dt and row.dt != source.end:
                row = next(source)
