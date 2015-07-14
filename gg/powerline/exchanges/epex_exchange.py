__author__ = "Warren"

from gg.powerline.assets.epex_metadata import EpexMetadata
from gg.powerline.utils import tradingcalendar_epex
from gg.powerline.sources.epex_source import EpexSource
from gg.powerline.exchanges.exchange import Exchange

from zipline.finance.commission import PerShare


class EpexExchange(Exchange):
    """
    Implementing abstractproperties for the EPEX exchange
    """
    @property
    def source(self):
        if self._source is None:
            self._source = EpexSource
        return self._source

    @property
    def asset_finder(self):
        if self._asset_finder is None:
            self._asset_finder = EpexMetadata().asset_finder
        return self._asset_finder

    @property
    def benchmark(self):
        if self._benchmark is None:
            self._benchmark = '^EPEX'
        return self._benchmark

    @property
    def calendar(self):
        if self._calendar is None:
            self._calendar = tradingcalendar_epex
        return self._calendar

    @property
    def commission(self):
        if self._commission is None:
            self._commission = PerShare(0.04)
        return self._commission
