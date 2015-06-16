from zipline.algorithm import TradingAlgorithm
from zipline.utils.api_support import api_method
from zipline.utils.events import StatelessRule

from gg.powerline.utils.tradingcalendar_epex import get_auctions


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


class AtAuction(StatelessRule):
    def __init__(self):
        self._dt = None

    def should_trigger(self, dt):
        return self._get_auction(dt)

    def _get_auction(self, dt):
        """
        Cache the auction for each day.
        """
        if self._dt is None or (self._dt.date() != dt.date()):
            self._dt = get_auctions(dt)

        return self._dt
