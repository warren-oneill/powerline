from zipline.algorithm import TradingAlgorithm
from zipline.utils.api_support import api_method
from zipline.utils.events import StatelessRule, _build_offset

import pandas as pd
from datetime import datetime, timedelta


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

    def current_universe(self):
        return self.insert_products()

    def insert_products(self):
        # TODO read from exchange
        # Incorporate QH products
        freq = 'H'
        index = 24

        return [freq + str(i) for i in range(1, index)]


class BeforeEpexAuction(StatelessRule):
    """
    A rule that triggers for some offset before the auction.
    Example that triggers triggers before 30 minutes of the auction close:

    BeforeEpexAuction(minutes=30)
    """
    def __init__(self, offset=None, **kwargs):
        self.offset = _build_offset(
            offset,
            kwargs,
            timedelta(minutes=1),  # Defaults to the first minute.
        )
        self._dt = None

    def should_trigger(self, dt):
        return (self._get_auction(dt) - self.offset).time() == dt.time()

    def _get_auction(self, dt):
        self._dt = self.get_auctions(dt)

        return self._dt

    # TODO: Incorpoate in calendar
    # TODO: remove day info
    def get_auctions(self, dt):
        """
        :param dt:
        :return: auction time on day=dt
        """
        auction = pd.Timestamp(datetime(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=12,
            minute=0),
            tz='Europe/Berlin').tz_convert('UTC')

        return auction
