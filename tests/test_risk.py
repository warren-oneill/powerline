from unittest import TestCase
import datetime

import pandas as pd
import numpy as np
import pytz
from zipline.utils.factory import create_simulation_parameters

from powerline.finance.risk import RiskReport

__author__ = "Warren, Max"


class TestRiskReport(TestCase):
    """
    Tests gg risk parameters.
    """
    @classmethod
    def setUpClass(cls):
        start = datetime.datetime(
            year=2006, month=1, day=1, tzinfo=pytz.utc)
        end = datetime.datetime(
            year=2006, month=1, day=10, tzinfo=pytz.utc)
        cls.period = pd.date_range(start, end)

        sim_params = create_simulation_parameters(start=start, end=end)
        sim_params.capital_base = 200
        perf = cls.create_mock_perf()
        cls.metrics = RiskReport(perf, sim_params)

    def test_var(self):
        """
        expected values calculated in excel, see
                                        tests/risk_scenario_and_VaR_calc.xlsx
        http://investexcel.net/calculating-value-at-risk-in-excel
        """
        expected_var_95 = 9.693259893
        expected_var_99 = 14.8464768
        expected_var_95_5_day = 14.08907233
        expected_var_99_5_day = 25.61201565
        expected_var_95_10_day = 11.88639228
        expected_var_99_10_day = 28.18229499

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
        expected_win_loss = 1.0
        self.assertEqual(self.metrics.win_loss, expected_win_loss)

    def test_absolute_benchmark(self):
        expected_benchmark_profit = 200 * 0.05232
        self.assertEqual(self.metrics.benchmark_profits,
                         expected_benchmark_profit)

    def test_longest_drawdown_duration(self):
        expected_drawdown_duration = 4
        self.assertEqual(self.metrics.longest_drawdown_duration,
                         expected_drawdown_duration)

    def test_display_report(self):
        self.metrics.display_report()

    def tearDown(self):
        self.returns = None
        self.sim_params = None
        self.perf = None
        self.metrics = None

    @classmethod
    def create_mock_perf(cls):
        # portfolio value = 200, 180, 144, 129.6, 259.2, 129.6, 285.12,
        #                   370.656, 111.1968, 130.100256

        returns = pd.Series([1, -0.1, -0.2, -0.1, 1, -0.5, 1.2, 0.3, -0.55,
                             0.27])
        pnl = pd.Series([0, -20, -36, -14.4, 129.6, -129.6, 155.52, 85.536,
                         -203.8608, 45.034704])
        max_drawdown = pd.Series([0, 0.1, 0.28, 0.352, 0.352, 0.5, 0.5, 0.5,
                                  0.55, 0.55])

        benchmark = pd.Series([0, 0.00169, 0.01798, 0.02976, 0.03387, 0.02803,
                               0.03703, 0.04380, 0.04553, 0.05232])

        # the following do not need to be tested as they are provided
        # by zipline
        returns_period = pd.Series(np.zeros(10))
        sortino = pd.Series(np.zeros(10))
        sharpe = pd.Series(np.zeros(10))
        information = pd.Series(np.zeros(10))

        return pd.DataFrame({'returns': returns,
                             'pnl': pnl,
                             'algorithm_period_return': returns_period,
                             'max_drawdown': max_drawdown,
                             'benchmark_period_return': benchmark,
                             'sortino': sortino,
                             'sharpe': sharpe,
                             'information': information}).\
            set_index(cls.period)
