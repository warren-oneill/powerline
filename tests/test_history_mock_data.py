__author__ = 'Max'

from unittest import TestCase

import numpy as np
import pandas as pd

from zipline.history.history import HistorySpec
from zipline.protocol import BarData
from zipline.finance.trading import TradingEnvironment

from gg.powerline.history.history_container import EpexHistoryContainer


class TestHistory(TestCase):
    @classmethod
    def setUpClass(cls):
        start_date = pd.Timestamp('2015-06-06', tz='Europe/Berlin').\
            tz_convert('UTC')
        end_date = pd.Timestamp('2015-06-10', tz='Europe/Berlin').\
            tz_convert('UTC')
        cls.days = pd.date_range(start_date, end_date)

        cls.env = TradingEnvironment()

        cls.bar_count = 3
        history_spec = HistorySpec(bar_count=cls.bar_count, frequency='1m',
                                   field='price', ffill=False,
                                   data_frequency='minute', env=cls.env)
        cls.history_specs = {}
        cls.history_specs[history_spec.key_str] = history_spec

        cls.market_forms = ['epex_auction', 'intraday', 'aepp', 'rebap']
        cls.hourly_products = ["%(a)02d-%(b)02d" % {'a': i, 'b': i+1}
                               for i in range(24)]
        cls.quarter_product_tags = ["Q"+str(i) for i in range(1, 5)]

    def setUp(self):
        self.container = EpexHistoryContainer(self.history_specs, None,
                                              self.days[0], 'minute',
                                              env=self.env)

    def test_full_data_content_batch_update(self):
        data = self.create_full_data()

        bar = BarData(data)
        self.container.update(bar, self.days[-1])
        history = self.container.get_history()

        for market in self.market_forms:
            self.assertLessEqual(len(history[market]), self.bar_count)

        for current_sid in data:
            current_data = data[current_sid]
            self.assertEqual(history[current_data['market']]
                             [current_data['product']].ix[current_data['day']],
                             current_data['price'])

    def test_sparse_data_content(self):
        data = self.create_sparse_data()

        for current_sid in data:
            current_data = data[current_sid]
            bar = BarData({current_sid: current_data})
            self.container.update(bar, self.days[-1])
            history = self.container.get_history()

            self.assertLessEqual(len(history[current_data['market']]),
                                 self.bar_count)

            self.assertEqual(history[current_data['market']]
                             [current_data['product']].ix[current_data['day']],
                             current_data['price'])

    def test_sparse_data_content_batch_update(self):
        data = self.create_sparse_data()

        bar = BarData(data)
        self.container.update(bar, self.days[-1])
        history = self.container.get_history()

        self.assertLessEqual(len(history['epex_auction']), self.bar_count)

        for current_sid in data:
            current_data = data[current_sid]
            if current_data['day'] not in self.days[-3:]:
                continue
            self.assertEqual(history[current_data['market']]
                             [current_data['product']].ix[current_data['day']],
                             current_data['price'])

    def test_sparse_data_final_dates(self):
        data = self.create_sparse_data()

        for current_sid in data:
            current_data = data[current_sid]
            bar = BarData({current_sid: current_data})
            self.container.update(bar, self.days[-1])

        history = self.container.get_history()
        observed_dates = history['epex_auction'].index.tolist()
        expected_dates = self.days[-3:]
        for i in range(3):
            self.assertEqual(observed_dates[i].date(),
                             expected_dates[i].date())

    def test_sparse_data_final_dates_batch_update(self):
        data = self.create_sparse_data()

        bar = BarData(data)
        self.container.update(bar, self.days[-1])
        history = self.container.get_history()

        observed_dates = history['epex_auction'].index.tolist()
        expected_dates = self.days[-3:]
        for i in range(3):
            self.assertEqual(observed_dates[i].date(),
                             expected_dates[i].date())

    def test_simple_price_update(self):
        data = self.create_simple_price_update_data()

        for current_sid in data:
            current_data = data[current_sid]
            bar = BarData({current_sid: current_data})
            self.container.update(bar, self.days[-1])

        history = self.container.get_history()

        self.assertEqual(history['aepp']['01Q1'].ix[self.days[0]], 7)
        self.assertEqual(history['aepp']['01Q1'].ix[self.days[1]], 10)

    def test_simple_price_update_batch_update(self):
        data = self.create_simple_price_update_data()

        bar = BarData(data)
        self.container.update(bar, self.days[-1])
        history = self.container.get_history()

        self.assertEqual(history['aepp']['01Q1'].ix[self.days[0]], 7)
        self.assertEqual(history['aepp']['01Q1'].ix[self.days[1]], 10)

    def test_dates_after_complex_update(self):
        data1, data2 = self.create_data_for_complex_update()

        for current_sid in data1:
            current_data = data1[current_sid]
            bar = BarData({current_sid: current_data})
            self.container.update(bar, self.days[-1])

        history = self.container.get_history()
        observed_dates = history['epex_auction'].index.tolist()
        expected_dates = [self.days[i] for i in [1, 2, 4]]
        for i in range(3):
            self.assertEqual(observed_dates[i].date(),
                             expected_dates[i].date())

        for current_sid in data2:
            current_data = data2[current_sid]
            bar = BarData({current_sid: current_data})
            self.container.update(bar, self.days[-1])

        history = self.container.get_history()
        observed_dates = history['epex_auction'].index.tolist()
        expected_dates = [self.days[i] for i in [2, 3, 4]]
        for i in range(3):
            self.assertEqual(observed_dates[i].date(),
                             expected_dates[i].date())

    def test_dates_after_complex_update_batch_update(self):
        data1, data2 = self.create_data_for_complex_update()

        bar = BarData(data1)
        self.container.update(bar, self.days[-1])
        history = self.container.get_history()

        observed_dates = history['epex_auction'].index.tolist()
        expected_dates = [self.days[i] for i in [1, 2, 4]]
        for i in range(3):
            self.assertEqual(observed_dates[i].date(),
                             expected_dates[i].date())

        bar = BarData(data2)
        self.container.update(bar, self.days[-1])
        history = self.container.get_history()

        observed_dates = history['epex_auction'].index.tolist()
        expected_dates = [self.days[i] for i in [2, 3, 4]]
        for i in range(3):
            self.assertEqual(observed_dates[i].date(),
                             expected_dates[i].date())

    def create_full_data(self):
        data = {}
        rolling_sid = 1
        for single_date in self.days[0:3]:
            for current_hour in range(24):
                data[rolling_sid] = {
                    'dt': self.days[-1],
                    'price': np.random.uniform(0, 100),
                    'market': self.market_forms[0],
                    'product': self.hourly_products[current_hour],
                    'day': single_date,
                    'sid': rolling_sid
                }
                rolling_sid += 1
                for market in self.market_forms[1:4]:
                    for current_quarter in self.quarter_product_tags:
                        data[rolling_sid] = {
                            'dt': self.days[-1],
                            'price': np.random.uniform(0, 100),
                            'market': market,
                            'product': "%02d" % current_hour + current_quarter,
                            'day': single_date,
                            'sid': rolling_sid
                        }
                        rolling_sid += 1

        return data

    def create_sparse_data(self):
        data = {}
        rolling_sid = 1
        for single_date in self.days:
            data[rolling_sid] = {
                'dt': self.days[-1],
                'price': np.random.uniform(0, 100),
                'market': 'epex_auction',
                'product': self.hourly_products[np.random.randint(0, 24)],
                'day': single_date,
                'sid': rolling_sid
            }
            rolling_sid += 1

        return data

    def create_simple_price_update_data(self):

        data = {1: {'dt': self.days[-1],
                    'price': 5,
                    'market': 'aepp',
                    'product': '01Q1',
                    'day': self.days[0],
                    'sid': 1},
                2: {'dt': self.days[-1],
                    'price': 10,
                    'market': 'aepp',
                    'product': '01Q1',
                    'day': self.days[1],
                    'sid': 2},
                3: {'dt': self.days[-1],
                    'price': 7,
                    'market': 'aepp',
                    'product': '01Q1',
                    'day': self.days[0],
                    'sid': 3}
                }

        return data

    def create_data_for_complex_update(self):
        data1 = {}
        rolling_sid = 1
        for i in [0, 1, 2, 4]:
            data1[rolling_sid] = {
                'dt': self.days[-1],
                'price': np.random.uniform(0, 100),
                'market': 'epex_auction',
                'product': '00-01',
                'day': self.days[i],
                'sid': rolling_sid
            }
            rolling_sid += 1
        data2 = {}
        for i in [2, 3, 4]:
            data2[rolling_sid] = {
                'dt': self.days[-1],
                'price': np.random.uniform(0, 100),
                'market': 'epex_auction',
                'product': '01-02',
                'day': self.days[i],
                'sid': rolling_sid
            }
            rolling_sid += 1

        return [data1, data2]
