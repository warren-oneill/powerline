__author__ = "Warren"

from gg.powerline.assets.epex_metadata import EpexMetadata
from gg.powerline.utils import tradingcalendar_epex
from gg.powerline.sources.epex_source import EpexSource
from gg.powerline.exchanges.exchange import Exchange

from gg.database.store import Store
from gg.powerline.settings import connection

from zipline.finance.commission import PerShare


class EpexExchange(Exchange):
    """
    Implementing abstractproperties for the EPEX exchange
    """
    @property
    def source(self):
        if self._source is None:
            self._source = EpexSource(start=self.start, end=self.end,
                                      env=self.env)
        return self._source

    @property
    def asset_metadata(self):
        if self._asset_metadata is None:
            self._asset_metadata = EpexMetadata(start=self.start,
                                                end=self.end).metadata
        return self._asset_metadata

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
            store = Store(connection(), create_new_engine=True)
            session = store.session
            self._products = {'hour': {}, 'qh': {}}
            # TODO rewrite with select distinct
            for products, day in session.execute(
                    'select GROUP_CONCAT(UPPER(TRADINGPRODUCT)), '
                    'date(CONVERT_TZ('
                    'BEGIN_TS, "UTC", "Europe/Berlin")) from EPEX_AUCTION '
                    'where EPEX_AUCTION.NAME '
                    '= "GermanPowerSpotAuction" and KIND like "Price%" '
                    'GROUP BY date('
                    'CONVERT_TZ('
                    'BEGIN_TS, "UTC", "Europe/Berlin"))').fetchall():
                self._products['hour'].update({str(day): products})

            for products, day in session.execute(
                    'select GROUP_CONCAT(UPPER(TRADINGPRODUCT)), '
                    'date(CONVERT_TZ('
                    'BEGIN_TS, "UTC", "Europe/Berlin")) from REBAP '
                    'where KIND like "energy%" GROUP BY date(CONVERT_TZ('
                    'BEGIN_TS, "UTC", "Europe/Berlin"))').fetchall():
                self._products['qh'].update({str(day): products})

            store.finalize()
        return self._products
