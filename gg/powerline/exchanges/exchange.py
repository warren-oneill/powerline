__author__ = "Warren"

from abc import ABCMeta, abstractproperty

from zipline.finance.trading import TradingEnvironment
from gg.powerline.data.loader_power import load_market_data


class Exchange(object, metaclass=ABCMeta):
    """
    A class to collect all exchange-relevant info.
    """
    def __init__(self):
        self._commission = None
        self._benchmark = None
        self._calendar = None
        self._asset_finder = None
        self._source = None

        self.exchange_tz = "Europe/Berlin"
        self.load = load_market_data
        self.env = self.insert_env()

    def insert_env(self):
        """
        passing relevant exchange objects to the environment
        """
        return TradingEnvironment(bm_symbol=self.benchmark,
                                  exchange_tz=self.exchange_tz,
                                  env_trading_calendar=self.calendar,
                                  load=self.load)

    @abstractproperty
    def source(self):
        """defined in subclass"""

    @abstractproperty
    def asset_finder(self):
        """defined in subclass"""

    @abstractproperty
    def benchmark(self):
        """defined in subclass"""

    @abstractproperty
    def calendar(self):
        """defined in subclass"""

    @abstractproperty
    def commission(self):
        """defined in subclass"""
