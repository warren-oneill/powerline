from zipline.algorithm import TradingAlgorithm
from zipline.utils.api_support import api_method
from zipline.utils.events import StatelessRule, _build_offset

from gg.powerline.utils.tradingcalendar_epex import get_auctions
from gg.powerline.assets.epex_metadata import EpexMetadata as emd

from datetime import timedelta
# TOTO name to general for auction specific code


class TradingAlgorithmGG(TradingAlgorithm):
    def insert_idents(self, day):
        idents = {}
        for i in range(1, 24):
            product = emd.insert_product(i)
            idents.update({i: emd.insert_ident(day, product)})

        return idents

    @api_method
    def order_auction(self, amounts, day):
        idents = self.insert_idents(day)

        for i in idents:
            self.order(self.symbol(idents[i]), amounts[i])

    def current_universe(self):
        return self.insert_products()

    def insert_products(self):
        # TODO make slicker
        # Incorporate QH products
        index = 24

        return [emd.insert_product(i) for i in range(1, index)]


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
        self._dt = get_auctions(dt)

        return self._dt
