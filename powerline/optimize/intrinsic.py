


# just playing.. not working (yet)



from datetime import datetime
import pytz
from zipline import TradingAlgorithm
from zipline.utils.factory import load_from_yahoo
from zipline.api import order, symbol, history


def example_init(self):
    self._buy_above = 400.0


class with_intrinsic_optimization(object):

     def __new__(cls, name, bases, attrs):
        attrs['__init__'] = example_init
        return super().__new__(cls, name, bases, attrs)


class OptimizedAlgorithm(TradingAlgorithm,
                       metaclass=with_intrinsic_optimization):

    def initialize(self):
        self._buy_above = 500.0

    def handle_data(self, data):
        if data[0]['price'] > self._buy_above:
            print("We buy above " + self._buy_above)
            order(symbol('GOOG'), 1)


if __name__ == '__main__':

    start = datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2015, 5, 31, 0, 0, 0, 0, pytz.utc)
    data = load_from_yahoo(stocks=['GOOG'],
                           start=start,
                           end=end)
    data = data.dropna()
    algo = OptimizedAlgorithm()
    results = algo.run(data)

