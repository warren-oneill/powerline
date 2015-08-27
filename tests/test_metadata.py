__author__ = "Warren"

import datetime
from unittest import TestCase

from zipline.assets.assets import Future
from zipline.assets.assets import AssetFinder

from gg.powerline.assets.epex_metadata import EpexMetadata
from gg.powerline.assets.eex_metadata import EexMetadata


class TestMetadataEex(TestCase):
    """
    Tests EEX weekly metadata.
    """
    def setUp(self):
        self.amd = EexMetadata().asset_finder

    def test_eex_metadata(self):
        self.assertIsInstance(self.amd, AssetFinder)
        for sid in self.amd.sids:
            self.assertIsInstance(self.amd.retrieve_asset(sid), Future)
            self.assertIsInstance(self.amd.retrieve_asset(sid).notice_date,
                                  datetime.date)
            self.assertIsInstance(self.amd.retrieve_asset(sid).expiration_date,
                                  datetime.date)
            self.assertIsInstance(self.amd.retrieve_asset(sid).
                                  contract_multiplier, int)
            self.assertGreater(self.amd.retrieve_asset(
                sid).contract_multiplier, 0)

    def tearDown(self):
        self.amd = None


class TestMetadataEpex(TestCase):
    """
    Tests EPEX hour product metadata.
    """
    def setUp(self):
        self.amd = EpexMetadata().asset_finder

    def test_epex_metadata(self):
        self.assertIsInstance(self.amd, AssetFinder)
        for sid in self.amd.sids:
            self.assertIsInstance(self.amd.retrieve_asset(sid), Future)
            self.assertIsInstance(self.amd.retrieve_asset(sid).notice_date,
                                  datetime.date)
            self.assertIsInstance(self.amd.retrieve_asset(sid).expiration_date,
                                  datetime.date)
            self.assertIsInstance(self.amd.retrieve_asset(sid).
                                  contract_multiplier, int)
            self.assertGreater(self.amd.retrieve_asset(
                sid).contract_multiplier, 0)

    def tearDown(self):
        self.amd = None
