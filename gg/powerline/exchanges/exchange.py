from abc import ABCMeta, abstractmethod

from zipline.finance.trading import TradingEnvironment
from zipline.finance.commission import PerShare

from gg.powerline.data.loader_power import load_market_data


class Exchange(object, metaclass=ABCMeta):
    """
    A class to collect all exchange-relevant info.
    """
    def __init__(self):
        self.bm_symbol = self.insert_bm()
        self.exchange_tz = "Europe/Berlin"
        self.calendar = self.insert_calendar()
        self.load = load_market_data
        self.commission = PerShare(self.insert_commission())
        self.env = self.insert_env()
        self.asset_finder = self.insert_asset_finder()
        self.source = self.insert_source()

    def insert_env(self):
        return TradingEnvironment(bm_symbol=self.bm_symbol,
                                  exchange_tz=self.exchange_tz,
                                  env_trading_calendar=self.calendar,
                                  load=self.load)

    @abstractmethod
    def insert_source(self):
        pass

    @abstractmethod
    def insert_asset_finder(self):
        pass

    @abstractmethod
    def insert_bm(self):
        pass

    @abstractmethod
    def insert_calendar(self):
        pass

    @abstractmethod
    def insert_commission(self):
        pass
