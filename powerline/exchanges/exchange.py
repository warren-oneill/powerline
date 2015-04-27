from zipline.finance import trading

from zipline.finance.trading import TradingEnvironment

from powerline.utils import tradingcalendar_eex
from powerline.sources.sql_source import SqlSource
from powerline.data.loader_power import load_market_data
from powerline.assets.eex_metadata import MetadataFromSql
from zipline.finance.commission import PerShare
from zipline.utils.factory import create_simulation_parameters


class Exchange():
    def __init__(self, kind, price_kind, calendar, commission):
        self.bm_symbol = '^EEX'
        self.exchange_tz = "Europe/Berlin"
        self.kind = kind
        self.price_kind = price_kind
        self.calendar = calendar
        self.load = load_market_data
        self.commission = PerShare(commission)

        trading.environment = self.insert_env()
        self.source = self.insert_source()
        self.sids = self.source.sids
        self.identifiers = self.source.identifiers
        self.metadata = self.insert_metadata()
        self.sim_params = create_simulation_parameters(start=self.source.start,
                                                       end=self.source.end)

    def insert_env(self):
        return TradingEnvironment(bm_symbol=self.bm_symbol,
                                  exchange_tz=self.exchange_tz,
                                  env_trading_calendar=self.calendar,
                                  load=self.load)

    def insert_source(self):
        return SqlSource(kind=self.kind, price_kind=self.price_kind)

    def insert_metadata(self):
        return MetadataFromSql()


EexExchange = Exchange(kind='Future',
                       price_kind='SettlementPrice',
                       calendar=tradingcalendar_eex,
                       commission=0.0125)
