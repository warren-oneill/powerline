'''
Defines trading days and trading times for the EEX weekly futures market.
'''

import pandas as pd

from datetime import datetime
from dateutil import rrule

from zipline.utils.tradingcalendar import end, canonicalize_datetime

start = pd.Timestamp('2013-01-01', tz='UTC')
end_base = pd.Timestamp('today', tz='UTC')


def get_non_trading_days(start, end):
    non_trading_rules = []

    start = canonicalize_datetime(start)
    end = canonicalize_datetime(end)

    weekends = rrule.rrule(
        rrule.YEARLY,
        byweekday=(rrule.SA, rrule.SU),
        cache=True,
        dtstart=start,
        until=end
    )
    non_trading_rules.append(weekends)
    # New Year's Day
    new_year = rrule.rrule(
        rrule.MONTHLY,
        byyearday=1,
        cache=True,
        dtstart=start,
        until=end
    )
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
    # Easter Monday
    easter_monday = rrule.rrule(
        rrule.DAILY,
        byeaster=1,
        cache=True,
        dtstart=start,
        until=end
    )
    non_trading_rules.append(easter_monday)
    # Christi Himmelfahrt
    ch_himm = rrule.rrule(
        rrule.DAILY,
        byeaster=39,
        cache=True,
        dtstart=pd.Timestamp('2013-01-01', tz='UTC'),
        until=pd.Timestamp('2013-12-31', tz='UTC')
    )
    non_trading_rules.append(ch_himm)
    # Pfingstmontag
    pfinst_mon = rrule.rrule(
        rrule.DAILY,
        byeaster=50,
        cache=True,
        dtstart=pd.Timestamp('2013-01-01', tz='UTC'),
        until=pd.Timestamp('2013-12-31', tz='UTC')
    )
    non_trading_rules.append(pfinst_mon)
    # Labour Day (1st of May)
    may_bank = rrule.rrule(
        rrule.MONTHLY,
        bymonth=5,
        bymonthday=1,
        cache=True,
        dtstart=start,
        until=end
    )
    non_trading_rules.append(may_bank)
    # Tag der Deutschen Einheit
    tde = rrule.rrule(
        rrule.MONTHLY,
        bymonth=10,
        bymonthday=3,
        cache=True,
        dtstart=pd.Timestamp('2013-01-01', tz='UTC'),
        until=pd.Timestamp('2013-12-31', tz='UTC')
    )
    non_trading_rules.append(tde)
    # Christmas Eve
    christmas_eve = rrule.rrule(
        rrule.MONTHLY,
        bymonth=12,
        bymonthday=24,
        cache=True,
        dtstart=start,
        until=end
    )
    non_trading_rules.append(christmas_eve)
    # Christmas Day
    christmas = rrule.rrule(
        rrule.MONTHLY,
        bymonth=12,
        bymonthday=25,
        cache=True,
        dtstart=start,
        until=end
    )
    non_trading_rules.append(christmas)
    # Boxing Day
    boxing_day = rrule.rrule(
        rrule.MONTHLY,
        bymonth=12,
        bymonthday=26,
        cache=True,
        dtstart=start,
        until=end
    )
    non_trading_rules.append(boxing_day)
    # New Year's Eve
    newyears_eve = rrule.rrule(
        rrule.MONTHLY,
        bymonth=12,
        bymonthday=31,
        cache=True,
        dtstart=start,
        until=end
    )
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
                hour=9,
                minute=31),
            tz='Europe/Berlin').tz_convert('UTC')
        # 1 PM if early close, 4 PM otherwise
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
