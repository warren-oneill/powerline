from zipline.api import order_target, symbol
from zipline.finance.commission import PerShare

from powerline.exchanges.exchange import EexExchange as exchange

ident = exchange.identifiers[3]


def initialize(self):
    self.i = 0
    self.set_commission(PerShare(0))


def handle_data(self, data):
    print(data, symbol(ident))
    if self.i < 1:
        order_target(symbol(ident), 1)
    self.i += 1
