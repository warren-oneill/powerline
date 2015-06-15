from gg.powerline.assets.epex_metadata import MetadataFromSqlEpex
from gg.powerline.utils import tradingcalendar_epex
from gg.powerline.sources.epex_source import EpexSource
from gg.powerline.exchanges.exchange import Exchange


class EpexExchange(Exchange):
    '''
    Implementing abstractmethods for the EPEX exchange
    '''
    def insert_source(self):
        return EpexSource

    def insert_asset_finder(self):
        return MetadataFromSqlEpex().asset_finder

    def insert_bm(self):
        return '^EPEX'

    def insert_calendar(self):
        return tradingcalendar_epex

    def insert_commission(self):
        return 0.04
