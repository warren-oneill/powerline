from zipline.finance.commission import PerShare

from powerline.utils import tradingcalendar_eex
from powerline.exchanges.exchange import Exchange

__author__ = "Warren"


class EexExchange(Exchange):
    """
    Implementing abstractproperties for the EEX exchange
    """

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

    @property
    def products(self):
        if self._products is None:
            self._products = ['F1B1', 'F1B2', 'F1B3', 'F1B4', 'F1B5']

        return self._products
