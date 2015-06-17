from zipline.algorithm import TradingAlgorithm
from zipline.utils.api_support import api_method
from zipline.utils.events import StatelessRule

import pandas as pd
from datetime import datetime


class TradingAlgorithmGG(TradingAlgorithm):
    def insert_idents(self, day, freq):
        if freq == 'H':
            index = 24
        else:
            index = 96

        idents = {}
        for i in range(1, index):
            idents.update({i: str(day) + '_' + freq + str(i)})

        return idents

    @api_method
    def order_auction(self, amounts, day, freq='H'):
        idents = self.insert_idents(day, freq)

        for i in idents:
            self.order(self.symbol(idents[i]), amounts[i])


class AtEpexAuction(StatelessRule):
    def __init__(self):
        self._dt = None

    def should_trigger(self, dt):
        return self._get_auction(dt)

    def _get_auction(self, dt):
        """
        Cache the auction for each day.
        """
        if self._dt is None or (self._dt.date() != dt.date()):
            self._dt = self.get_auctions(dt)

        return self._dt

    # TODO: Incorpoate in calendar (generates error)
    def get_auctions(self, dt):
        auction = pd.Timestamp(datetime(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=12,
            minute=0),
            tz='Europe/Berlin').tz_convert('UTC')

        return auction
