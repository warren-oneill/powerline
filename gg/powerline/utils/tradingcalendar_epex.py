'''
Defines trading days and trading times for the EPEX market.
'''


import pandas as pd
from datetime import datetime

from zipline.utils.tradingcalendar import end, canonicalize_datetime

canonicalize_datetime = canonicalize_datetime

start = pd.Timestamp('2013-01-01', tz='UTC')
end_base = pd.Timestamp('today', tz='UTC')

non_trading_days = []
trading_day = pd.tseries.offsets.CDay(holidays=non_trading_days)


def get_trading_days(start, end, trading_day=trading_day):
    return pd.date_range(start=start.date(),
                         end=end.date(),
                         freq='D').tz_localize('UTC')

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
                hour=0,
                minute=0),
            tz='Europe/Berlin').tz_convert('UTC')
        market_close = pd.Timestamp(
            datetime(
                year=day.year,
                month=day.month,
                day=day.day,
                hour=23,
                minute=59),
            tz='Europe/Berlin').tz_convert('UTC')

        open_and_closes.loc[day, 'market_open'] = market_open
        open_and_closes.loc[day, 'market_close'] = market_close

    return open_and_closes

open_and_closes = get_open_and_closes(trading_days, early_closes)
