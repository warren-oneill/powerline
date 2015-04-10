__author__ = 'warren'
from zipline.finance import trading

from powerline.finance.trading import TradingEnvironment

from powerline.utils import tradingcalendar_eex as calendar
from powerline.sources.eex_source import SqlSource
from powerline.data.loader_power import load_market_data
from powerline.assets.eex_metadata import MetadataFromSql
from zipline.finance.commission import PerShare


class EexExchange():
    def __init__(self):
        self.bm_symbol = '^EEX'
        self.exchange_tz = "Europe/Berlin"
        self.env_trading_calendar = calendar
        self.load = load_market_data
        self.commission = PerShare(0.0125)

        trading.environment = self.insert_env()
        self.source = self.insert_source()
        self.sids = self.source.sids
        self.metadata = self.insert_metadata()

    def insert_env(self):
        return TradingEnvironment(bm_symbol=self.bm_symbol,
                                  exchange_tz=self.exchange_tz,
                                  env_trading_calendar=self.env_trading_calendar,
                                  load=self.load)

    def insert_source(self):
        return SqlSource()

    def insert_metadata(self):
        return MetadataFromSql()
