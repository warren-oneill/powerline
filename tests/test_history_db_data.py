__author__ = 'Warren'

from unittest import TestCase
import pandas as pd

from zipline.history.history import HistorySpec
from zipline.protocol import BarData

from gg.powerline.history.history_container import EpexHistoryContainer
from gg.powerline.exchanges.epex_exchange import EpexExchange


class TestHistory(TestCase):

    def setUp(self):
        start = pd.Timestamp('2015-06-25', tz='Europe/Berlin').tz_convert(
            'UTC')
        end = pd.Timestamp('2015-06-30', tz='Europe/Berlin').tz_convert('UTC')

        self.exchange = EpexExchange(start=start, end=end)
        self.env = self.exchange.env
        self.env.write_data(futures_data=self.exchange.asset_metadata)

        self.source = self.exchange.source
        history_spec = HistorySpec(bar_count=2, frequency='1m', field='price',
                                   ffill=False,
                                   data_frequency='minute', env=self.env)
        history_specs = {}
        history_specs[history_spec.key_str] = history_spec

        self.container = EpexHistoryContainer(history_specs, None,
                                              self.source.start, 'minute',
                                              env=self.env)

    def test_history(self):
        # TODO test previous values
        for row in self.source:
            dt = row['day']
            data = {row['sid']: dict(row)}

            bar = BarData(data)
            self.container.update(bar, row['dt'])
            history = self.container.get_history()

            if row['market'] in ['cascade', 'auction_signal']:
                continue
>>>>>>> 17b3353... New history tests in _alt, with mock data

            self.assertLessEqual(len(history[row['market']]), 2)

            self.assertEqual(history[row['market']][row['product']].ix[dt],
                             row['price'], history[
                                 row['market']][row['product']])

    def tearDown(self):
        pass
