__author__ = "Warren"

from abc import ABCMeta, abstractproperty
import pandas as pd
from datetime import datetime

from zipline.finance.trading import TradingEnvironment
from gg.powerline.data.loader_power import load_market_data


class Exchange(object, metaclass=ABCMeta):
    """
    A class to collect all exchange-relevant info.
    """

    def __init__(self,
                 start=pd.Timestamp(datetime(day=1, month=1, year=2013),
                                    tz='UTC'),
                 end=pd.Timestamp(datetime(day=31, month=12, year=2015),
                                  tz='UTC')):
        self._commission = None
        self._benchmark = None
        self._calendar = None
        self._asset_metadata = None
        self._source = None
        self._env = None
        self._products = None
        self.start = start
        self.end = end

        self.exchange_tz = "Europe/Berlin"
        self.load = load_market_data

    @property
    def env(self):
        """
        passing relevant exchange objects to the environment
        """
        if self._env is None:
            self._env = TradingEnvironment(bm_symbol=self.benchmark,
                                           exchange_tz=self.exchange_tz,
                                           env_trading_calendar=self.calendar,
                                           load=self.load)
        return self._env

    @abstractproperty
    def source(self):
        """defined in subclass"""

    @abstractproperty
    def asset_metadata(self):
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
