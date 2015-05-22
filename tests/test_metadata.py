from powerline.exchanges.exchange import EexExchange

import datetime
from unittest import TestCase

from zipline.assets.assets import Future

amd_eex = EexExchange.asset_finder


class TestMetadata(TestCase):

    def setUp(self):
        self.amd = amd_eex

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
