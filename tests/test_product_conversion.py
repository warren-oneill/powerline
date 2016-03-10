import pandas as pd
import numpy as np

from unittest import TestCase

from powerline.utils.hour_quarter_hour_converter import \
    convert_between_h_and_qh

from powerline.exchanges.epex_exchange import EpexExchange

__author__ = "Max"


class TestProductConversion(TestCase):
    """
    Testing the utility function for history conversion via mock histories
    """

    def setUp(self):
        exchange = EpexExchange()
        self.hourly_products = exchange.products['hour']
        self.quarterly_products = exchange.products['qh']

    def test_conversion_hourly_to_quarterly(self):
        hourly_data = np.array([range(0, 24), range(24, 48), range(48, 72)])
        hourly_history = pd.DataFrame(hourly_data,
                                      columns=self.hourly_products,
                                      index=pd.date_range('2015-01-01',
                                                          '2015-01-03'))

        quarterly_row_0 = np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
                                    3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
                                    6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9,
                                    9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11,
                                    12, 12, 12, 12, 13, 13, 13, 13,
                                    14, 14, 14, 14, 15, 15, 15, 15,
                                    16, 16, 16, 16, 17, 17, 17, 17,
                                    18, 18, 18, 18, 19, 19, 19, 19,
                                    20, 20, 20, 20, 21, 21, 21, 21,
                                    22, 22, 22, 22, 23, 23, 23, 23])

        quarterly_row_1 = quarterly_row_0 + 24
        quarterly_row_2 = quarterly_row_0 + 48
        quarterly_data = np.array([quarterly_row_0, quarterly_row_1,
                                   quarterly_row_2])

        expected_output = pd.DataFrame(quarterly_data,
                                       columns=self.quarterly_products,
                                       index=pd.date_range('2015-01-01',
                                                           '2015-01-03'))

        observed_output = convert_between_h_and_qh(hourly_history)

        self.assertTrue(observed_output.equals(expected_output))

    def test_conversion_quarterly_to_hourly(self):
        quarterly_data = np.array([range(0, 96), range(96, 192), range(192,
                                                                       288)])
        quarterly_history = pd.DataFrame(quarterly_data,
                                         columns=self.quarterly_products,
                                         index=pd.date_range('2015-01-01',
                                                             '2015-01-03'))
        hourly_data = np.array([range(0, 24), range(24, 48), range(48, 72)]) \
            * 4 + 1.5

        expected_output = pd.DataFrame(hourly_data,
                                       columns=self.hourly_products,
                                       index=pd.date_range('2015-01-01',
                                                           '2015-01-03'))

        observed_output = convert_between_h_and_qh(quarterly_history)

        self.assertTrue(observed_output.equals(expected_output))

    def test_no_history(self):
        no_history = pd.DataFrame(np.random.randn(3, 3))

        self.assertRaises(ValueError, convert_between_h_and_qh, no_history)
