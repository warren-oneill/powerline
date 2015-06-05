from zipline.api import order_target, symbol
from zipline.finance.commission import PerShare
from zipline.finance.performance.position import positiondict
from zipline.finance.performance.position_tracker import PositionTracker

from powerline.utils.data.data_generator import DataGeneratorEpex
from powerline.exchanges.exchange import EpexExchange as exchange

ident = exchange.identifiers[3]

dg = DataGeneratorEpex(identifier=ident)
_, df = dg.create_data()


def initialize(self):
    self.i = 0
    self.set_commission(PerShare(0))


def handle_data(self, data):
    if self.i < 1:
        order_target(symbol(ident), 1)
    self.i += 1
