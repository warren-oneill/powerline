from powerline.assets.epex_metadata import MetadataFromSqlEpex
from powerline.utils import tradingcalendar_epex
from powerline.sources.sql_source import EpexSource
from powerline.exchanges.exchange import Exchange


class EpexExchange(Exchange):
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