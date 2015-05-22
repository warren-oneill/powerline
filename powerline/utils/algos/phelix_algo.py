from zipline.algorithm import TradingAlgorithm
from zipline.api import order_target, symbol
from zipline.finance.commission import PerShare


from powerline.exchanges.exchange import EexExchange as exchange

sid = exchange.sids[3]
ident = exchange.identifiers[3]


def initialize(self):
    self.i = 0
    self.set_commission(PerShare(0))


def handle_data(self, data):
    print(data, symbol(ident))
    if self.i < 1:
        order_target(symbol(ident), 1)
    self.i += 1


algo = TradingAlgorithm(initialize=initialize,
                        handle_data=handle_data,
                        asset_finder=exchange.asset_finder,
                        sim_params=exchange.sim_params,
                        instant_fill=True)
