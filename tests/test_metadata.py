__author__ = "Warren"

import datetime
from unittest import TestCase

from zipline.assets.assets import Future

from gg.powerline.assets.epex_metadata import EpexMetadata
from gg.powerline.assets.eex_metadata import EexMetadata


class TestMetadataEex(TestCase):
    """
    Tests EEX weekly metadata.
    """
    def setUp(self):
        self.amd = EexMetadata().asset_finder

    def test_eex_metadata(self):
        self.assertNotEqual(self.amd.metadata_cache, None)
        for index in self.amd.metadata_cache:
            self.assertIsInstance(self.amd.retrieve_asset(index), Future)
            self.assertIsInstance(self.amd.retrieve_asset(index).notice_date,
                                  datetime.date)
            self.assertIsInstance(self.amd.retrieve_asset(index).expiration_date,
                                  datetime.date)
            self.assertIsInstance(self.amd.retrieve_asset(index).contract_multiplier,
                                  int)
            self.assertGreater(self.amd.retrieve_asset(index).contract_multiplier, 0)

    def tearDown(self):
        self.amd = None


class TestMetadataEpex(TestCase):
    """
    Tests EPEX hour product metadata.
    """
    def setUp(self):
        self.amd = EpexMetadata().metadata

    def test_epex_metadata(self):
        self.assertNotEqual(self.amd, None)
        for index in self.amd:
            self.assertEqual(self.amd[index]['asset_type'], 'future')
            self.assertIsInstance(self.amd[index]['notice_date'],
                                  datetime.date)
            self.assertIsInstance(self.amd[index]['expiration_date'],
                                  datetime.date)
            self.assertIsInstance(self.amd[index]['contract_multiplier'],
                                  int)
            self.assertGreater(self.amd[index]['contract_multiplier'], 0)

    def tearDown(self):
        self.amd = None
