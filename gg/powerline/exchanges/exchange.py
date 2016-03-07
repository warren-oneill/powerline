from abc import ABCMeta, abstractproperty, abstractmethod

from zipline.finance.trading import TradingEnvironment
from gg.powerline.data.loader_power import load_market_data


__author__ = "Warren, Stefan"


class Exchange(object, metaclass=ABCMeta):
    """
    A class to collect all exchange-relevant info.
    """

    def __init__(self, **kwargs):
        self._commission = None
        self._benchmark = None
        self._calendar = None
        self._type = kwargs.get("type", None)
        self._env = None
        self._products = kwargs.get("products", None)
        self.exchange_tz = "Europe/Berlin"
        self.load = load_market_data

    @property
    def env(self):
        """
        passing relevant exchange objects to the environment
        """
        if self._env is None:
            self._env = TradingEnvironment(
                bm_symbol=self.benchmark,
                exchange_tz=self.exchange_tz,
                env_trading_calendar=self.calendar,
                load=self.load)
        return self._env

    @abstractproperty
    def benchmark(self):
        """defined in subclass"""

    @abstractproperty
    def calendar(self):
        """defined in subclass"""

    @abstractproperty
    def commission(self):
        """defined in subclass"""

    def insert_ident(self, day, product):
        return str(day) + '_' + product