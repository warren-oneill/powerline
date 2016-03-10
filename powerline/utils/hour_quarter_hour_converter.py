import pandas as pd
import numpy as np
from itertools import product

__author__ = 'max'

hourly_products = ['%02d-%02d' % (i, i + 1) for i in range(24)]
quarter_tags = ['Q%d' % i for i in range(1, 5)]
quarterly_products = ['%02d%s' % (i, tag)
                      for (i, tag) in product(range(24), quarter_tags)]


def convert_between_h_and_qh(source_frame):
    """
    Convert a DataFrame with hourly or quarter hour price data to the other
    format
    :param source_frame: DataFrame with hourly or quarter hour prices
    :return: DataFrame with quarter hour or hourly prices
    """
    if source_frame.columns.shape[0] == 24:
        result_frame = pd.DataFrame(np.array(source_frame).repeat(4, axis=1),
                                    index=source_frame.index,
                                    columns=quarterly_products)
    elif source_frame.columns.shape[0] == 96:
        data = np.array(source_frame)
        mean_data = np.mean(np.array([data[:, ::4], data[:, 1::4],
                                      data[:, 2::4], data[:, 3::4]]), axis=0)
        result_frame = pd.DataFrame(mean_data, index=source_frame.index,
                                    columns=hourly_products)
    else:
        raise ValueError('Argument source_frame should be a Dataframe with ' +
                         'either 24 or 96 columns')
    return result_frame
