__author__ = "Warren"

from gg.powerline.utils import tradingcalendar_epex
from gg.powerline.exchanges.exchange import Exchange

from zipline.finance.commission import PerShare

import pandas as pd


class EpexExchange(Exchange):
    """
    Implementing abstractproperties for the EPEX exchange
    """
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

    @property
    def products(self):
        if self._products is None:
            self._products = {'hour': {}, 'qh': {}}
            self._products['hour'] = ["%(a)02d-%(b)02d" % {'a': i, 'b': i+1}
                               for i in range(24)]
            self._products['qh'] = [str(j).zfill(2) + "Q"+str(i) for i in range(1, 5) for j in range(24)]

        return self._products
