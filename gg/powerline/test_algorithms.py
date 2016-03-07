import pandas as pd
from zipline.algorithm import TradingAlgorithm
from gg.powerline.finance.auction import TradingAlgorithmAuction, \
    BeforeEpexAuction


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


class TestFekAlgo(TestAuctionAlgorithm):

    def initialize(self,
                   sid,
                   amount,
                   order_count,
                   day,
                   products,
                   sid_filter=None,
                   slippage=None,
                   commission=None):
        self.count = order_count
        self.asset = self.sid(sid)
        self.amount = amount
        self.day = day
        self.incr = 0
        self.products = products
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
        self.prog_update(data, self.datetime)

    def auction(self, data):
        self.order_auction(amounts=self.amount)


class FlippingAlgorithm(TradingAlgorithm):

    def initialize(self,
                   sid,
                   amount,
                   slippage,
                   commission):
        self.asset = self.sid(sid)
        self.amount = amount
        self.sid_filter = [self.asset.sid]
        self.set_slippage(slippage)
        self.set_commission(commission)

    def handle_data(self, data):

        if len(self.portfolio.positions) > 0:
            if self.portfolio.positions[self.asset.sid]["amount"] > 0:
                self.order_target(self.asset, -self.amount)
            else:
                self.order_target(self.asset, 0)
        else:
            self.order_target(self.asset, self.amount)
