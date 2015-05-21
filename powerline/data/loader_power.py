import pandas as pd
from math import pow
import numpy as np

from zipline.data.loader import dump_treasury_curves, get_data_filepath

from powerline.utils.tradingcalendar_eex import trading_day as trading_day_eex
from powerline.utils.tradingcalendar_eex import trading_days \
    as trading_days_eex

INDEX_MAPPING = {
    '^GSPC':
    ('treasuries', 'treasury_curves.csv', 'data.treasury.gov'),
    '^GSPTSE':
    ('treasuries_can', 'treasury_curves_can.csv', 'bankofcanada.ca'),
    '^FTSE':  # use US treasuries until UK bonds implemented
    ('treasuries', 'treasury_curves.csv', 'data.treasury.gov'),
}


def load_market_data(trading_day=trading_day_eex,
                     trading_days=trading_days_eex, bm_symbol='^EEX'):
    # generate constant daily returns for an annualised rate of 12%
    daily_return = pow(1.12, 1.0/365.0) - 1
    benchmark_returns = pd.Series(daily_return, index=trading_days)

    sd = 0.001
    for dt, value in benchmark_returns.iteritems():
        benchmark_returns[dt] = value + np.random.randn() * sd

    most_recent = pd.Timestamp('today', tz='UTC') - trading_day
    most_recent_index = trading_days.searchsorted(most_recent)
    days_up_to_now = trading_days[:most_recent_index + 1]

    # Get treasury curve module, filename & source from mapping.
    # Default to USA.
    module, filename, source = INDEX_MAPPING.get(
        bm_symbol, INDEX_MAPPING['^GSPC'])

    tr_filepath = get_data_filepath(filename)
    try:
        saved_curves = pd.DataFrame.from_csv(tr_filepath)
    except (OSError, IOError):
        print("""
data files aren't distributed with source.
Fetching data from {0}
""".format(source).strip())
        dump_treasury_curves(module, filename)
        saved_curves = pd.DataFrame.from_csv(tr_filepath)

    # Find the offset of the last date for which we have trading data in our
    # list of valid trading days
    last_tr_date = saved_curves.index[-1]
    last_tr_date_offset = days_up_to_now.searchsorted(
        last_tr_date.strftime('%Y/%m/%d'))

    # If more than 1 trading days has elapsed since the last day where
    # we have data,then we need to update
    # Comment above explains why this is "> 2".
    if len(days_up_to_now) - last_tr_date_offset > 2:
        treasury_curves = dump_treasury_curves(module, filename)
    else:
        treasury_curves = saved_curves.tz_localize('UTC')

    # tr_curves = {}
    # for tr_dt, curve in treasury_curves.T.iteritems():
    #     # tr_dt = tr_dt.replace(hour=0, minute=0, second=0, microsecond=0,
    #     #                       tzinfo=pytz.utc)
    #     tr_curves[tr_dt] = curve.to_dict()
    #
    # tr_curves = OrderedDict(sorted(
    #     ((dt, c) for dt, c in iteritems(tr_curves)),
    #     key=lambda t: t[0]))

    treasury_curves = treasury_curves.reindex(trading_days, method='ffill')
    return benchmark_returns, treasury_curves
