__author__ = "Warren"

from unittest import TestCase
import datetime

import pandas as pd
import numpy as np
import pytz

from gg.powerline.finance.risk_gg import RiskReport


class TestRiskReport(TestCase):
    """
    Tests gg risk parameters.
    """

    def setUp(self):
        self.perf = self.create_mock_perf()

        self.metrics = RiskReport(self.perf)

    def test_var(self):
        """
        expected values calculated in excel. see VaR-cal.xlsx
        http://investexcel.net/calculating-value-at-risk-in-excel
        """
        expected_var_95 = 6.87574503
        expected_var_99 = 10.6897709
        expected_var_95_5_day = 8.9352718397
        expected_var_99_5_day = 17.4636929683
        expected_var_95_10_day = 5.8126066176
        expected_var_99_10_day = 17.8736154433

        self.assertAlmostEqual(self.metrics.var_95, expected_var_95)
        self.assertAlmostEqual(self.metrics.var_99, expected_var_99)
        self.assertAlmostEqual(self.metrics.five_day_var_95,
                               expected_var_95_5_day)
        self.assertAlmostEqual(self.metrics.five_day_var_99,
                               expected_var_99_5_day)
        self.assertAlmostEqual(self.metrics.calculate_var(0.95, 10),
                               expected_var_95_10_day)
        self.assertAlmostEqual(self.metrics.calculate_var(0.99, 10),
                               expected_var_99_10_day)

    def test_win_loss(self):
        expected_win_loss = 1.33

        self.assertEqual(self.metrics.win_loss, expected_win_loss)

    def test_display_report(self):
        self.metrics.display_report()

    def tearDown(self):
        self.returns = None
        self.sim_params = None
        self.perf = None
        self.metrics = None

    def create_mock_perf(self):
        start = datetime.datetime(
            year=2006,
            month=1,
            day=1,
            hour=0,
            minute=0,
            tzinfo=pytz.utc)
        end = datetime.datetime(
            year=2006, month=1, day=7, tzinfo=pytz.utc)

        period = pd.date_range(start, end)

        # portfolio value = 200, 100, 180, 210.6, 421.2, 379.8, 208.494
        returns = pd.Series([1.0, -0.5, 0.8, .17, 1.0, -0.1, -0.45])
        pnl = pd.Series([0, -100, 80, 20.6, 220.6, -41.4, -171.306])
        benchmark = pd.Series([200, 204, 205, 203, 204, 206, 208])
        max_drawdown = pd.Series([0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.495])

        # the following do not need to be tested as they are provided
        # by zipline
        returns_period = pd.Series(np.zeros(7))
        sortino = pd.Series(np.zeros(7))
        sharpe = pd.Series(np.zeros(7))
        information = pd.Series(np.zeros(7))

        return pd.DataFrame({'returns': returns,
                             'pnl': pnl,
                             'algorithm_period_return': returns_period,
                             'max_drawdown': max_drawdown,
                             'benchmark_period_return': benchmark,
                             'sortino': sortino,
                             'sharpe': sharpe,
                             'information': information}).set_index(period)
