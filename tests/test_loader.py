from unittest import TestCase
import os

from zipline.data.loader import get_data_filepath, INDEX_MAPPING

from powerline.data.loader_power import load_market_data
from powerline.utils.tradingcalendar_eex import trading_day, trading_days

__author__ = "Warren"


class TestLoader(TestCase):

    def setUp(self):
        bm_symbol = '^EEX'
        _, filename, _ = INDEX_MAPPING.get(
            bm_symbol, INDEX_MAPPING['^GSPC'])

        tr_filepath = get_data_filepath(filename)
        os.remove(tr_filepath)
        self.benchmark, self.treasury = load_market_data(trading_day,
                                                         trading_days)

    def test_loader(self):
        for i, day in enumerate(self.benchmark.index):
            self.assertEqual(day, trading_days[i])
            self.assertEqual(day, self.treasury.index[i])

    def tearDown(self):
        pass
