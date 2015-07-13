from gg.powerline.finance.auction import TradingAlgorithmGG, BeforeEpexAuction
from gg.messaging.json_producer import JsonProducer

from datetime import timedelta


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

        self.schedule_function(func=auction, time_rule=BeforeEpexAuction(
            minutes=30))

    def handle_data(self, data):
        pass


def auction(algo, data):
    """
    Calculates the current day and then places an auction order for the
    following day.
    """
    day = algo.get_datetime().date() + timedelta(days=1)
    algo.order_auction(day=day, amounts=algo.amount)
    algo.incr += 1


class TestEpexMessagingAlgorithm(TradingAlgorithmGG):
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

        self.schedule_function(func=auction_message,
                               time_rule=BeforeEpexAuction(minutes=30))

        self.producer = JsonProducer()

    def handle_data(self, data):
        self.producer.run(self.datetime.date(),
                          self.perf_tracker.cumulative_performance.pnl)


def auction_message(algo, data):
    """
    Calculates the current day and then places an auction order for the
    following day.
    """
    day = algo.get_datetime().date() + timedelta(days=1)
    algo.order_auction(day=day, amounts=algo.amount)
    algo.incr += 1
