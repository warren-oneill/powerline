import pandas as pd

from powerline.finance.auction import TradingAlgorithmAuction, \
    BeforeEpexAuction

__author__ = 'Warren'


class TestAuctionAlgorithm(TradingAlgorithmAuction):
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

        self.prog = pd.DataFrame()

        if sid_filter:
            self.sid_filter = sid_filter
        else:
            self.sid_filter = [self.asset.sid]

        if slippage is not None:
            self.set_slippage(slippage)

        if commission is not None:
            self.set_commission(commission)

        self.schedule_function(func=self.auction, time_rule=BeforeEpexAuction(
            minutes=30))

    def handle_data(self, data):
        pass
