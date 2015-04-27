from powerline.exchanges.exchange import EexExchange

import datetime
from unittest import TestCase

amd_eex = EexExchange.metadata


class TestMetadata(TestCase):
    def setUp(self):
        self.amd = amd_eex

    def test_eex_metadata(self):
        self.assertNotEqual(self.amd.cache, None)
        for index in self.amd.cache:
            self.assertEqual(self.amd.cache[index]['asset_type'], 2)
            self.assertIsInstance(self.amd.cache[index]['notice_date'],
                                  datetime.date)
            self.assertIsInstance(self.amd.cache[index]['expiration_date'],
                                  datetime.date)
            self.assertIsInstance(self.amd.cache[index]['contract_multiplier'],
                                  int)
            self.assertGreater(self.amd.cache[index]['contract_multiplier'], 0)

    def tearDown(self):
        self.amd = None
