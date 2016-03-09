from datetime import timedelta

from zipline.algorithm import TradingAlgorithm
from zipline.utils.api_support import api_method
from zipline.utils.events import StatelessRule, _build_offset
import numpy as np

from powerline.utils.tradingcalendar_epex import get_auctions
from powerline.exchanges.epex_exchange import EpexExchange

__author__ = 'Warren'


class TradingAlgorithmAuction(TradingAlgorithm):

    def __init__(self, *args, **kwargs):
        if kwargs.get('auction'):
            self.auction = kwargs.pop('auction')
        else:
            raise ValueError('You must define an auction function.')
        self.exchange = EpexExchange()
        self.products = self.exchange.products
        super().__init__(*args, **kwargs)

    @api_method
    def order_auction(self, amounts):
        day = self.get_datetime().date() + timedelta(days=1)
        amounts = np.concatenate((amounts, [0]))
        for i, product in enumerate(self.products['hour']):
            ident = self.exchange.insert_ident(day, product)
            self.order_target(self.future_symbol(ident), amounts[i])


def auction(algo, data):

    algo.order_auction(amounts=algo.amount)


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
            timedelta(minutes=60),  # Defaults to the first minute.
        )
        self._dt = None

    def should_trigger(self, dt, env):
        return (self._get_auction(dt) - self.offset).time() == dt.time()

    def _get_auction(self, dt):
        self._dt = get_auctions(dt)

        return self._dt
