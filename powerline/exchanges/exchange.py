from zipline.finance.trading import TradingEnvironment

from powerline.utils import tradingcalendar_eex, tradingcalendar_epex

from powerline.sources.sql_source import EexSource, EpexSource
from powerline.data.loader_power import load_market_data
from powerline.assets.eex_metadata import MetadataFromSql
from zipline.finance.commission import PerShare
from zipline.utils.factory import create_simulation_parameters


class Exchange():
    def __init__(self, data_source, bm_symbol, calendar, commission):
        self.bm_symbol = bm_symbol
        self.exchange_tz = "Europe/Berlin"
        self.calendar = calendar
        self.load = load_market_data
        self.commission = PerShare(commission)
        self.env = self.insert_env()
        self.asset_finder = self.insert_metadata()
        self.data_source = data_source
        self.source = self.insert_source()
        self.sids = self.source.sids
        self.identifiers = self.source.identifiers
        self.sim_params = create_simulation_parameters(start=self.source.start,
                                                       end=self.source.end)

    def insert_env(self):
        return TradingEnvironment(bm_symbol=self.bm_symbol,
                                  exchange_tz=self.exchange_tz,
                                  env_trading_calendar=self.calendar,
                                  load=self.load)

    def insert_source(self):
        return self.data_source()

    def insert_metadata(self):
        return MetadataFromSql().asset_finder


EexExchange = Exchange(data_source=EexSource, bm_symbol='^EEX',
                       calendar=tradingcalendar_eex,
                       commission=0.0125)

EpexExchange = None  # Exchange(data_source=EpexSource, bm_symbol='^EPEX',
                     #    calendar=tradingcalendar_epex,
                     #    commission=0.04)  # TODO Epex commission
