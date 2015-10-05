__author__ = "Warren"

from datetime import date, datetime
from unittest import TestCase
import pandas as pd

from zipline.assets.assets import Future
from zipline.assets.assets import AssetFinder

from gg.powerline.exchanges.eex_exchange import EexExchange
from gg.powerline.exchanges.epex_exchange import EpexExchange


class TestMetadataEex(TestCase):
    """
    Tests EEX weekly metadata.
    """

    def setUp(self):
        start = pd.Timestamp(datetime(day=10, month=10, year=2014), tz='UTC')
        end = pd.Timestamp(datetime(day=11, month=10, year=2014), tz='UTC')

        exchange = EexExchange(start=start, end=end)
        env = exchange.env
        self.amd = env.asset_finder

    def test_eex_metadata(self):
        for sid in self.amd.sids:
            asset = self.amd.retrieve_asset(sid)
            self.assertIsInstance(asset, Future)
            self.assertIsInstance(asset.notice_date, date)
            self.assertIsInstance(asset.expiration_date, date)
            self.assertIsInstance(asset.contract_multiplier, float)
            self.assertGreater(asset.contract_multiplier, 0)
            self.assertEqual(asset.exchange, 'EEX')
            self.assertEqual(asset.root_symbol, 'F1B')
            self.assertEqual(asset.asset_name, 'Phelix Weekly Base')

    def tearDown(self):
        self.amd = None


class TestMetadataEpex(TestCase):
    """
    Tests EPEX hour product metadata.
    """

    def setUp(self):
        start = pd.Timestamp(datetime(day=10, month=10, year=2014), tz='UTC')
        end = pd.Timestamp(datetime(day=12, month=10, year=2014), tz='UTC')

        exchange = EpexExchange(start=start, end=end)
        env = exchange.env
        env.write_data(futures_data=exchange.asset_metadata)

        self.amd = env.asset_finder

    def test_epex_metadata(self):
        self.assertIsInstance(self.amd, AssetFinder)
        for sid in self.amd.sids:
            asset = self.amd.retrieve_asset(sid)
            self.assertIsInstance(asset, Future)
            self.assertIsInstance(asset.notice_date, date)
            self.assertIsInstance(asset.expiration_date, date)
            self.assertIsInstance(asset.end_date, date)

            day = asset.end_date.tz_convert(
                'Europe/Berlin').date()
            dt = asset.end_date - asset.expiration_date
            if day < date(2015, 7, 16):
                self.assertEqual(dt.seconds / 60, 45)
            else:
                self.assertEqual(dt.seconds / 60, 30)

            self.assertIsInstance(asset.contract_multiplier, float)
            self.assertGreater(asset.contract_multiplier, 0)

    def tearDown(self):
        self.amd = None
