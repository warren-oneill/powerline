__author__ = "Warren"

from gg.powerline.utils import tradingcalendar_eex
from gg.powerline.exchanges.exchange import Exchange
from gg.powerline.sources.eex_source import EexSource
from gg.powerline.assets.eex_metadata import MetadataFromSqlEex


class EexExchange(Exchange):
    """
    Implementing abstractmethods for the EEX exchange
    """
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
