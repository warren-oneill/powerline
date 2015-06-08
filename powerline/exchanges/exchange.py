from zipline.finance.trading import TradingEnvironment
from zipline.finance.commission import PerShare

from powerline.data.loader_power import load_market_data


class Exchange(object):
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

    def insert_source(self):
        return {}

    def insert_asset_finder(self):
        return {}

    def insert_bm(self):
        return {}

    def insert_calendar(self):
        return {}

    def insert_commission(self):
        return {}

# TODO please instantiate (once) where needed
# e.g. specific exchange could be a borg
# https://github.com/faif/python-patterns/blob/master/borg.py
# returned from a factory
# https://github.com/faif/python-patterns/blob/master/factory_method.py
# EexExchange = Exchange(data_source=EexSource,
#                        meta_data_obj=MetadataFromSqlEex,
#                        bm_symbol='^EEX',
#                        calendar=tradingcalendar_eex,
#                        commission=0.0125)
#
# EpexExchange = Exchange(data_source=EpexSource, bm_symbol='^EPEX',
#                         meta_data_obj=MetadataFromSqlEpex,
#                         calendar=tradingcalendar_epex,
#                         commission=0.04)
