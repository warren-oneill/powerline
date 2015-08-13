__author__ = "Warren"

import datetime
import time
from unittest import TestCase

from zipline.assets.assets import Future

from gg.powerline.exchanges.eex_exchange import EexExchange
from gg.powerline.exchanges.epex_exchange import EpexExchange
from gg.powerline.assets.epex_metadata import EpexMetadata
from gg.powerline.assets.eex_metadata import EexMetadata


class TestMetadataEex(TestCase):
    """
    Tests EEX weekly metadata.
    """
    def setUp(self):
        # self.exchange = EexExchange()
        self.amd = EexMetadata().asset_finder # self.exchange.asset_finder

    def test_eex_metadata(self):
        self.assertNotEqual(self.amd.cache, None)
        for index in self.amd.cache:
            self.assertIsInstance(self.amd.cache[index], Future)
            self.assertIsInstance(self.amd.cache[index].notice_date,
                                  datetime.date)
            self.assertIsInstance(self.amd.cache[index].expiration_date,
                                  datetime.date)
            self.assertIsInstance(self.amd.cache[index].contract_multiplier,
                                  int)
            self.assertGreater(self.amd.cache[index].contract_multiplier, 0)

    def tearDown(self):
        self.amd = None


class TestMetadataEpex(TestCase):
    """
    Tests EPEX hour product metadata.
    """
    def setUp(self):
        self.start = time.time()
        self.amd = EpexMetadata().asset_finder

    def test_epex_metadata(self):
        self.assertNotEqual(self.amd.cache, None)
        for index in self.amd.cache:
            self.assertIsInstance(self.amd.cache[index], Future)
            self.assertIsInstance(self.amd.cache[index].notice_date,
                                  datetime.date)
            self.assertIsInstance(self.amd.cache[index].expiration_date,
                                  datetime.date)
            self.assertIsInstance(self.amd.cache[index].contract_multiplier,
                                  int)
            self.assertGreater(self.amd.cache[index].contract_multiplier, 0)

    def tearDown(self):
        print(time.time() - self.start)
        self.amd = None
