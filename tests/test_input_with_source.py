from datetime import datetime
import pandas as pd
from unittest import TestCase
from gg.powerline.exchanges.eex_exchange import EexExchange


class TestEexSourceWithInput(TestCase):

    @classmethod
    def setUpClass(cls):
        pass
        # cls.start = pd.Timestamp(datetime(day=20, month=6, year=2015),
        #                          tz='Europe/Berlin').tz_convert('UTC')
        # cls.end = pd.Timestamp(datetime(day=25, month=6, year=2015),
        #                        tz='Europe/Berlin').tz_convert('UTC')
        # cls.exchange = EexExchange(start=cls.start, end=cls.end, products=[
        #     'F1B1', 'F1B2'])
        # cls.exchange.env.write_data(
        #     futures_data=cls.exchange.asset_metadata)

    def test_input_source(self):
        pass
        # source = self.exchange.source
        # self.assertIsInstance(source.start, pd.lib.Timestamp)
        # self.assertIsInstance(source.end, pd.lib.Timestamp)
        # last_dt = self.start
        # for event in source:
        #     self.assertIsInstance(event.dt, date)
        #     self.assertGreaterEqual(event.dt, last_dt)
        #     self.assertIsInstance(event.volume, int)
        #     self.assertGreater(event.volume, 0)
        #     self.assertIsInstance(event.sid, int)
        #     self.assertIsInstance(event.price, float)
        #     self.assertIn(event.product, ['F1B1', 'F1B2'])
        #
        #     self.assertTrue(abs(event.price) >= 0.01 or abs(event.price) == 0)
        #     self.assertGreaterEqual(event.dt, self.start)
        #     self.assertLessEqual(event.dt, self.end)

    @classmethod
    def tearDownClass(cls):
        pass
