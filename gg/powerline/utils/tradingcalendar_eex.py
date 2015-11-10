__author__ = "Warren"

"""
Defines trading days and trading times for the EEX weekly futures market.
"""

import pandas as pd

from datetime import datetime
from dateutil import rrule

from zipline.utils.tradingcalendar import end, canonicalize_datetime

from gg.powerline.utils.global_calendar import (
    boxing_day, ch_himm, christmas, christmas_eve, easter_monday, may_bank,
    new_year, newyears_eve, pfinst_mon_13, pfinst_mon_15, tde, weekends
)

start = pd.Timestamp('2010-12-01', tz='UTC')
end_base = pd.Timestamp('today', tz='UTC')


def get_non_trading_days(start, end):
    non_trading_rules = []

    start = canonicalize_datetime(start)
    end = canonicalize_datetime(end)

    non_trading_rules.append(weekends)

    non_trading_rules.append(new_year)
    # Good Friday
    good_friday = rrule.rrule(
        rrule.DAILY,
        byeaster=-2,
        cache=True,
        dtstart=start,
        until=end
    )
    non_trading_rules.append(good_friday)

    non_trading_rules.append(easter_monday)

    non_trading_rules.append(ch_himm)

    non_trading_rules.append(pfinst_mon_13)

    non_trading_rules.append(pfinst_mon_15)

    non_trading_rules.append(may_bank)

    non_trading_rules.append(tde)

    non_trading_rules.append(christmas_eve)

    non_trading_rules.append(christmas)

    non_trading_rules.append(boxing_day)

    non_trading_rules.append(newyears_eve)

    non_trading_ruleset = rrule.rruleset()
    for rule in non_trading_rules:
        non_trading_ruleset.rrule(rule)
    non_trading_days = non_trading_ruleset.between(start, end, inc=True)

    non_trading_days.sort()
    return pd.DatetimeIndex(non_trading_days)

non_trading_days = get_non_trading_days(start, end)
trading_day = pd.tseries.offsets.CDay(holidays=non_trading_days)


def get_trading_days(start, end, trading_day=trading_day):
    return pd.date_range(start=start.date(),
                         end=end.date(),
                         freq=trading_day).tz_localize('UTC')

trading_days = get_trading_days(start, end)


def get_early_closes(start, end):
    '''
    we have no early closes but its needed within zipline
    '''
    return []

early_closes = get_early_closes(start, end)


def get_open_and_closes(trading_days, early_closes):
    open_and_closes = pd.DataFrame(index=trading_days,
                                   columns=('market_open', 'market_close'))
    for day in trading_days:
        market_open = pd.Timestamp(
            datetime(
                year=day.year,
                month=day.month,
                day=day.day,
                hour=8,
                minute=00),
            tz='Europe/Berlin').tz_convert('UTC')
        close_hour = 18
        market_close = pd.Timestamp(
            datetime(
                year=day.year,
                month=day.month,
                day=day.day,
                hour=close_hour),
            tz='Europe/Berlin').tz_convert('UTC')

        open_and_closes.loc[day, 'market_open'] = market_open
        open_and_closes.loc[day, 'market_close'] = market_close

    return open_and_closes

open_and_closes = get_open_and_closes(trading_days, early_closes)
