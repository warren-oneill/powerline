
from powerline.utils import tradingcalendar_eex
from powerline.exchanges.exchange import Exchange
from powerline.sources.sql_source import EexSource
from powerline.assets.eex_metadata import MetadataFromSqlEex


class EexExchange(Exchange):
    def insert_source(self):
        return EexSource

    def insert_asset_finder(self):
        return MetadataFromSqlEex().asset_finder

    def insert_bm(self):
        return '^EEX'

    def insert_calendar(self):
        return tradingcalendar_eex

    def insert_commission(self):
        return 0.0125