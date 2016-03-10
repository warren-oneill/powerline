from unittest import TestCase

import numpy as np
import pandas as pd
from zipline.history.history import HistorySpec
from zipline.protocol import BarData
from zipline.finance.trading import TradingEnvironment

from powerline.history.history_container import EpexHistoryContainer

__author__ = 'Max'


class TestHistory(TestCase):
    """
    Testing the powerline history, mainly throught mock data. These data are
     created in the create_* functions below the test_* functions.
    """
    @classmethod
    def setUpClass(cls):
        """
        sets up the objects which can be used during all the tests. This avoids
        reinitialising commonly used objects.
        """
        start_date = pd.Timestamp('2015-07-06', tz='Europe/Berlin').\
            tz_convert('UTC')
        end_date = pd.Timestamp('2015-07-10', tz='Europe/Berlin').\
            tz_convert('UTC')
        cls.days = pd.date_range(start_date, end_date)

        cls.env = TradingEnvironment()

        cls.bar_count = 3
        history_spec = HistorySpec(bar_count=cls.bar_count, frequency='1m',
                                   field='price', ffill=False,
                                   data_frequency='minute', env=cls.env)
        cls.history_specs = {}
        cls.history_specs[history_spec.key_str] = history_spec

        cls.market_forms = ['epex_auction', 'intraday']
        cls.hourly_products = ["%(a)02d-%(b)02d" % {'a': i, 'b': i + 1}
                               for i in range(24)]
        cls.quarter_product_tags = ["Q" + str(i) for i in range(1, 5)]

    def setUp(self):
        """
        Initializing the history container for each individual test.
        """
        self.container = EpexHistoryContainer(self.history_specs, None,
                                              self.days[0], 'minute',
                                              env=self.env)

    def test_full_data_content(self):
        """
        Testing the history with a full set of data over three days, i.e. the
        contains values for all in 'epex_auction', 'intraday'
        and for all appropriate time periods.
        """
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
        """
        Testing whether the entries in the history are correct, when created
         from a small set of data, containing only 'epex_auction' prices for
         one period over five days.

        This test updates creates the history one data entry at a time. A batch
         update is tested in another routine.
        """
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
        """
        Testing whether the entries in the history are correct, when created
         from a small set of data, containing only 'epex_auction' prices for
         one period over five days.

        This test updates creates the history in one go. An entrywise creation
         is tested in other routine.
        """
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
        """
        Testing whether the dates in the history are correct, when created
         from a small set of data, containing only 'epex_auction' prices for
         one period over five days.

        This test updates creates the history one data entry at a time. A batch
         update is tested in another routine.
        """
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
        """
        Testing whether the dates in the history are correct, when created
         from a small set of data, containing only 'epex_auction' prices for
         one period over five days.

        This test updates creates the history in one go. An entrywise creation
         is tested in other routine.
        """
        data = self.create_sparse_data()

        bar = BarData(data)
        self.container.update(bar, self.days[-1])
        history = self.container.get_history()

        observed_dates = history['epex_auction'].index.tolist()
        expected_dates = self.days[-3:]
        for i in range(3):
            self.assertEqual(observed_dates[i].date(),
                             expected_dates[i].date())

    def test_dates_after_complex_update(self):
        """
        Testing dates in the history after an update with somewhat complicated
         data configurations.

        This test updates creates the history one data entry at a time. A batch
         update is tested in another routine.
        """
        data1, data2, test_data = self.create_data_for_complex_update()

        for current_sid in data1:
            current_data = data1[current_sid]
            bar = BarData({current_sid: current_data})
            self.container.update(bar, self.days[-1])

        history = self.container.get_history()
        observed_dates = history['epex_auction'].index.tolist()
        expected_dates = [self.days[i] for i in [0, 2, 4]]
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

        for sid in test_data:
            current_data = test_data[sid]
            current_date = current_data['day']
            current_product = current_data['product']

            observed_price = \
                history['epex_auction'][current_product][current_date]
            expected_price = current_data['price']
            self.assertEqual(observed_price, expected_price)

        self.assertTrue(np.isnan(
            history['epex_auction']['00-01'][self.days[3]]))
        self.assertTrue(np.isnan(
            history['epex_auction']['02-03'][self.days[4]]))

    def test_dates_after_complex_update_batch_update(self):
        """
        Testing dates in the history after an update with somewhat complicated
         data configurations.

        This test updates creates the history in one go. An entrywise creation
         is tested in other routine.
        """
        data1, data2, test_data = self.create_data_for_complex_update()

        bar = BarData(data1)
        self.container.update(bar, self.days[-1])
        history = self.container.get_history()

        observed_dates = history['epex_auction'].index.tolist()
        expected_dates = [self.days[i] for i in [0, 2, 4]]
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

        for sid in test_data:
            current_data = test_data[sid]
            current_date = current_data['day']
            current_product = current_data['product']

            observed_price = \
                history['epex_auction'][current_product][current_date]
            expected_price = current_data['price']
            self.assertEqual(observed_price, expected_price)

        self.assertTrue(np.isnan(
            history['epex_auction']['00-01'][self.days[3]]))
        self.assertTrue(np.isnan(
            history['epex_auction']['02-03'][self.days[4]]))

    def test_edge_cases(self):
        """
        Test cases where nothing is added to the history.
        """

        # Create deep copy of empyt history for comparison
        history = self.container.get_history()
        empty_history_copy = {}
        for market in history.keys():
            empty_history_copy[market] = history[market].copy()

        data1, data2 = self.create_edge_case_data()

        # Test empty data
        bar = BarData(data1)
        self.container.update(bar, self.days[-1])
        history = self.container.get_history()

        for market in history.keys():
            self.assertTrue(history[market].equals(empty_history_copy[market]))

        # Test 'cascade' and 'auction_signal'
        bar = BarData(data2)
        self.container.update(bar, self.days[-1])
        history = self.container.get_history()

        for market in history.keys():
            self.assertTrue(history[market].equals(empty_history_copy[market]))

    def create_full_data(self):
        """
        Create a set of complete data for three days. With all price types and
        for all periods.

        :return: A set of mock data.
        """
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
        """
        Create a small set of data, containing only one price for
        'epex_auction' for 5 days in a row

        :return: A set of mock data.
        """
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

    def create_data_for_complex_update(self):
        """
        Create two sets of data where the second set updates upon the first one
         both by introducing a new date which lies within the recordable time
         frame.

        :return: two individual sets of mock data
        """
        data1 = {}
        rolling_sid = 1
        for i in [0, 2, 4]:
            data1[rolling_sid] = {
                'dt': self.days[-1],
                'price': np.random.uniform(0, 100),
                'market': 'epex_auction',
                'product': '00-01',
                'day': self.days[i],
                'sid': rolling_sid
            }
            rolling_sid += 1
            data1[rolling_sid] = {
                'dt': self.days[-1],
                'price': np.random.uniform(0, 100),
                'market': 'epex_auction',
                'product': '01-02',
                'day': self.days[i],
                'sid': rolling_sid
            }
            rolling_sid += 1

        data2 = {}
        for i in [1, 2, 3]:
            data2[rolling_sid] = {
                'dt': self.days[-1],
                'price': np.random.uniform(0, 100),
                'market': 'epex_auction',
                'product': '01-02',
                'day': self.days[i],
                'sid': rolling_sid
            }
            rolling_sid += 1
            data2[rolling_sid] = {
                'dt': self.days[-1],
                'price': np.random.uniform(0, 100),
                'market': 'epex_auction',
                'product': '02-03',
                'day': self.days[i],
                'sid': rolling_sid
            }
            rolling_sid += 1

        test_data = {}
        for i in [3, 5, 6]:
            test_data[i] = data1[i]
        for i in range(9, 13):
            test_data[i] = data2[i]

        return [data1, data2, test_data]

    def create_edge_case_data(self):
        """
        Create two data sets which will not be recorded in the history.

        :return: two individual sets of mock data
        """
        data1 = {}

        data2 = {1: {'dt': self.days[-1],
                     'price': np.random.uniform(0, 100),
                     'market': 'cascade',
                     'product': '00-01',
                     'day': self.days[0],
                     'sid': 1},
                 2: {'dt': self.days[-1],
                     'price': np.random.uniform(0, 100),
                     'market': 'auction_signal',
                     'product': '00-01',
                     'day': self.days[0],
                     'sid': 2}}

        return [data1, data2]
