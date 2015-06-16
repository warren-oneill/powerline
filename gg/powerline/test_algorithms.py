from gg.powerline.finance.auction import TradingAlgorithmGG, AtEpexAuction

from datetime import timedelta
from gg.powerline.finance.auction import TradingAlgorithmGG


class TestAuctionAlgorithm(TradingAlgorithmGG):
    """
    This algorithm will send a specified number of orders, to allow unit tests
    to verify the orders sent/received, transactions created, and positions
    at the close of a simulation.
    """
    def initialize(self,
                   sid,
                   amount,
                   order_count,
                   day,
                   sid_filter=None,
                   slippage=None,
                   commission=None):
        self.count = order_count
        self.asset = self.sid(sid)
        self.amount = amount
        self.day = day
        self.incr = 0

        if sid_filter:
            self.sid_filter = sid_filter
        else:
            self.sid_filter = [self.asset.sid]

        if slippage is not None:
            self.set_slippage(slippage)

        if commission is not None:
            self.set_commission(commission)

    def handle_data(self, data):
        # place an order for amount shares of sid
        if self.incr < self.count:
            self.order_auction(day=self.day, amounts=self.amount)
            self.incr += 1

def auction(algo, data):
    day = algo.get_datetime().date() + timedelta(days=1)
    algo.order_auction(day=day, amounts=algo.amount)
    algo.incr += 1
