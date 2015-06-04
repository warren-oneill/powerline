from zipline.algorithm import TradingAlgorithm

#   TODO pls add doc strings for each class and for each method
class AlgoWrapper():

    def __init__(self, exchange, optimize, initialize, handle_data):
        # TODO type """ and hit return to enter standard documentation for methods
        self.exchange = exchange
        self.optimize = optimize
        self.algo = TradingAlgorithm(initialize=initialize,
                                     handle_data=handle_data,
                                     commission=exchange.commission,
                                     asset_metadata=exchange.metadata)

    def run_algo(self):
        pass
