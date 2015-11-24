__author__ = "Warren"

import pandas as pd
from math import pow
import numpy as np

from zipline.data.loader import ensure_treasury_data

INDEX_MAPPING = {
    '^GSPC':
    ('treasuries', 'treasury_curves.csv', 'data.treasury.gov'),
    '^GSPTSE':
    ('treasuries_can', 'treasury_curves_can.csv', 'bankofcanada.ca'),
    '^FTSE':  # use US treasuries until UK bonds implemented
    ('treasuries', 'treasury_curves.csv', 'data.treasury.gov'),
}


def load_market_data(trading_day,
                     trading_days, bm_symbol='^EEX'):
    """
    A patch of zipline loader which using the trading_days to generate a
    constant benchmark and treasury curve that matches the market days.

    :param trading_day:
    :param trading_days:
    :param bm_symbol:
    :return: benchmark, treasury
    """
    # generate constant daily returns for an annualised rate of 12%
    daily_return = pow(1.12, 1.0 / 365.0) - 1
    benchmark_returns = pd.Series(daily_return, index=trading_days)
    # now = pd.Timestamp.utcnow()

    sd = 0.001
    for dt, value in benchmark_returns.iteritems():
        benchmark_returns[dt] = value + np.random.randn() * sd

    first_date = trading_days[0]
    last_date = trading_days[
        trading_days.get_loc(pd.Timestamp.utcnow(), method='ffill') - 2
    ]
    treasury_curves = ensure_treasury_data(
        bm_symbol,
        first_date,
        last_date,
        # now,
    )
    treasury_curves = treasury_curves.reindex(trading_days, method='ffill')

    return benchmark_returns, treasury_curves
