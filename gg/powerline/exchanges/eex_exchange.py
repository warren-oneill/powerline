__author__ = "Warren"

from gg.powerline.utils import tradingcalendar_eex
from gg.powerline.exchanges.exchange import Exchange
from gg.powerline.sources.eex_source import EexSource
from gg.powerline.assets.eex_metadata import MetadataFromSqlEex
from zipline.finance.commission import PerShare


class EexExchange(Exchange):
    """
    Implementing abstract methods for the EEX exchange
    """

    def __init__(self):

        self._commission = None
        super().__init__()

    def insert_source(self):
        return EexSource

    def insert_asset_finder(self):
        return MetadataFromSqlEex().asset_finder

    def insert_bm(self):
        return '^EEX'

    def insert_calendar(self):
        return tradingcalendar_eex

    def commission(self):
        if self._commission is None:
            self._commission = PerShare(0.0125)
        else:
            return self._commission
