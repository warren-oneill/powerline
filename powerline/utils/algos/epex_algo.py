from zipline.api import order_target, symbol
from zipline.finance.commission import PerShare

from powerline.exchanges.epex_exchange import EpexExchange

ident = EpexExchange().source().identifiers[3]


def initialize(self):
    self.i = 0
    self.set_commission(PerShare(0))


def handle_data(self, data):
    if self.i < 1:
        order_target(symbol(ident), 1)
    self.i += 1
