__author__ = 'max'

import pandas as pd
import numpy as np
from itertools import product

hourly_products = ['%02d-%02d' % (i, i+1) for i in range(24)]
quarter_tags = ['Q%d' % i for i in range(1, 5)]
quarterly_products = ['%02d%s' % (i, tag)
                      for (i, tag) in product(range(24), quarter_tags)]


def convert_h_to_qh(h_data):
    """
    Convert a DataFrame containing hourly price data (e.g. the history of
    'epex_auction') into one with quarter hour prices by copying one hour's
    prices into it's four associated quarters
    :param h_data: DataFrame with the hourly price data
    :return: DataFrame with quarter hour prices
    """
    qh_data = pd.DataFrame(np.array(h_data).repeat(4, axis=1),
                           index=h_data.index, columns=quarterly_products)
    return qh_data


def convert_qh_to_h(qh_data):
    """
    Convert a DataFrame containing quarter hour prices (e.g. the history of
    'aepp') into one with hourly prices by averaging the prices
    :param qh_data: DataFrame with the quarter hour price
    :return: DataFrame with hourly prices
    """
    data = np.array(qh_data)
    mean_data = np.mean(np.array([data[:, ::4], data[:, 1::4],
                                  data[:, 2::4], data[:, 3::4]]), axis=0)
    h_data = pd.DataFrame(mean_data,
                          index=qh_data.index, columns=hourly_products)
    return h_data
