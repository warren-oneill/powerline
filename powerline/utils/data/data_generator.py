from datetime import timedelta

from zipline.sources import DataPanelSource
from zipline.protocol import DATASOURCE_TYPE
import pandas as pd
import numpy as np

from powerline.finance.auction import get_auctions

__author__ = "Warren"


class DataGeneratorEex(object):
    """
    Generates test EEX weekly data.
    """

    def __init__(self, identifier, env, instant_fill):
        self.env = env
        self.ident = identifier
        self.sid = \
            self.env.asset_finder.lookup_future_symbol(
                self.ident).sid
        self.instant_fill = instant_fill

    def create_simple(self):
        expir = self.env.asset_finder.retrieve_asset(
            self.sid).expiration_date
        day = pd.Timestamp(expir, tz='UTC').tz_convert('Europe/Berlin').date()
        first_day = self.env.next_trading_day(day)
        ix = self.env.trading_days.get_loc(first_day)
        days = self.env.trading_days[ix - 4:ix]
        index = [self.env.get_open_and_close(pd.Timestamp(
            d, tz='UTC').tz_convert('Europe/Berlin'))[1] for d in days]

        # prices
        x = [1, 5, 10, np.nan]
        data = pd.DataFrame([
            [1, 1e9, int(DATASOURCE_TYPE.TRADE)],
            [5, 168, int(DATASOURCE_TYPE.TRADE)],
            [10, 0, int(DATASOURCE_TYPE.CLOSE_POSITION)],
            [np.nan, 0, int(DATASOURCE_TYPE.TRADE)]],
            columns=['price', 'volume', 'type'], index=index)
        pan = pd.Panel({self.sid: data})
        if self.instant_fill:
            pnl = pd.DataFrame(
                [0, 0, (x[1] - x[0]) * 168, (x[2] - x[1]) * 168],
                index=index, columns=[self.ident])
            expected_positions = pd.DataFrame(
                [0, 1, 1, 0], index=index)
        else:
            pnl = pd.DataFrame([0, 0, 0, (x[2] - x[1]) * 168],
                               index=index, columns=[self.ident])
            expected_positions = pd.DataFrame(
                [0, 0, 1, 0], index=index)

        return DataPanelSource(pan), pnl, expected_positions


class DataGeneratorEpex(object):
    """
    Generates test EPEX  auction and intraday
    """

    def __init__(self, identifier, env):
        self.env = env
        self.ident = identifier
        self.sid = \
            self.env.asset_finder.lookup_future_symbol(
                self.ident).sid
        children = self.env.asset_finder.lookup_future_symbol(self.ident
                                                              ).children
        self.sid_qh = [self.env.asset_finder.
                       lookup_future_symbol(i).sid
                       for i in children]

    def create_data(self):
        expir = self.env.asset_finder.retrieve_asset(
            self.sid).expiration_date
        day = pd.Timestamp(expir, tz='UTC').tz_convert('Europe/Berlin').date()

        auction_ts = get_auctions(day) - timedelta(days=1)
        intraday_ts = auction_ts + timedelta(days=1)

        index = [auction_ts - timedelta(minutes=30),  # scheduler triggers
                 # 30min before auction close
                 auction_ts,
                 auction_ts + timedelta(minutes=30),
                 intraday_ts]

        # PNL timestamps are at market close. i.e. 00:00 local time
        index_pnl = [self.env.get_open_and_close(pd.Timestamp(
                     auction_ts, tz='UTC').tz_convert('Europe/Berlin'))[1],
                     self.env.get_open_and_close(pd.Timestamp(
                         intraday_ts, tz='UTC'
                     ).tz_convert('Europe/Berlin'))[1]]

        prices = [0, 1, 5]
        prices_qh = [[-2, 6, 6, 10]]
        products = ['01Q1', '01Q2', '01Q3', '01Q4']

        # price, volume, type, product
        product = '01-02'  # TODO defer from metadata
        data_h = pd.DataFrame([[prices[0], 0, int(DATASOURCE_TYPE.TRADE),
                                product, 'auction_signal'],
                               [prices[1], 1e9, int(DATASOURCE_TYPE.TRADE),
                                product, 'epex_auction'],
                               [np.nan, 0,
                                int(DATASOURCE_TYPE.CASCADE_POSITION),
                                product, 'cascade']],
                              columns=['price', 'volume', 'type', 'product',
                                       'market'],
                              index=index[0:3])
        trade_dict = {self.sid: data_h}
        for i, j in enumerate(self.sid_qh):
            data_qh = pd.DataFrame(
                [[prices_qh[0][i], 0, DATASOURCE_TYPE.TRADE, products[i],
                  'intraday']],
                columns=['price', 'volume', 'type', 'product', 'market'],
                index=[index[-1]])

            trade_dict.update({j: data_qh})

        pan = pd.Panel.from_dict(trade_dict)

        pnl = pd.DataFrame([0, (prices[2] - prices[1])],
                           index=index_pnl, columns=[self.ident])

        return DataPanelSource(pan), pnl
