__author__ = "Warren"

from gg.powerline.utils import tradingcalendar_eex
from gg.powerline.exchanges.exchange import Exchange
from gg.powerline.sources.eex_source import EexSource
from gg.powerline.assets.eex_metadata import MetadataFromSqlEex

from zipline.finance.commission import PerShare


class EexExchange(Exchange):
    """
    Implementing abstractproperties for the EEX exchange
    """
    @property
    def source(self):
        if self._source is None:
            self._source = EexSource
        return self._source

    @property
    def asset_finder(self):
        if self._asset_finder is None:
            self._asset_finder = MetadataFromSqlEex().asset_finder
        return self._asset_finder

    @property
    def benchmark(self):
        if self._benchmark is None:
            self._benchmark = '^EEX'
        return self._benchmark

    @property
    def calendar(self):
        if self._calendar is None:
            self._calendar = tradingcalendar_eex
        return self._calendar

    @property
    def commission(self):
        if self._commission is None:
            self._commission = PerShare(0.0125)
        return self._commission
