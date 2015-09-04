from zipline.algorithm import TradingAlgorithm
from zipline.utils.api_support import api_method
from zipline.utils.events import StatelessRule, _build_offset

from gg.powerline.utils.tradingcalendar_epex import get_auctions
from gg.powerline.assets.epex_metadata import EpexMetadata as emd

from datetime import timedelta
# TODO take idents from metadata in algo (need daily)


class TradingAlgorithmAuction(TradingAlgorithm):
    @api_method
    def order_auction(self, amounts, day):
        # #TODO make products part of class
        for i, product in enumerate(self.products['hour'][str(day)].
                                    split(sep=',')):
            ident = emd.insert_ident(day, product)
            self.order(self.symbol(ident), amounts[i])


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
