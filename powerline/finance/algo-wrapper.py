__author__ = 'warren'

from zipline.algorithm import TradingAlgorithm


class AlgoWrapper():
    def __init__(self, exchange, optimize, initialize, handle_data):
        self.exchange = exchange
        self.optimize = optimize
        self.algo = TradingAlgorithm(initialize=initialize,
                            handle_data=handle_data,
                            commission=exchange.commission,
                            asset_metadata=exchange.metadata)

    def run_algo(self):
        pass