__author__ = "Warren"

from gg.powerline.assets.epex_metadata import MetadataFromSqlEpex
from gg.powerline.utils import tradingcalendar_epex
from gg.powerline.sources.epex_source import EpexSource
from gg.powerline.exchanges.exchange import Exchange
from zipline.finance.commission import PerShare


class EpexExchange(Exchange):
    """
    Implementing abstractmethods for the EPEX exchange
    """
    def insert_source(self):
        return EpexSource

    def insert_asset_finder(self):
        return MetadataFromSqlEpex().asset_finder

    def insert_benchmark(self):
        return '^EPEX'

    def insert_calendar(self):
        return tradingcalendar_epex

    def commission(self):
        if self._commission is None:
            self._commission = PerShare(0.04)
        else:
            return self._commission
