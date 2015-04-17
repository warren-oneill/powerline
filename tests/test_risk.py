from unittest import TestCase

import pandas as pd
import datetime
import pytz

from zipline.finance.trading import SimulationParameters

from powerline.finance.risk_gg import RiskReport


class TestRiskReport(TestCase):
    def setUp(self):
        self.perf = self.create_mock_perf()

        self.metrics = RiskReport(self.perf)

    def test_var(self):
        # expected values calculated in excel. see VaR-cal.xlsx
        # http://investexcel.net/calculating-value-at-risk-in-excel
        expected_var_95 = 6.87574503
        expected_var_99 = 10.6897709

        self.assertAlmostEqual(self.metrics.var_95, expected_var_95)
        self.assertAlmostEqual(self.metrics.var_99, expected_var_99)

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
        start_date = datetime.datetime(
            year=2006,
            month=1,
            day=1,
            hour=0,
            minute=0,
            tzinfo=pytz.utc)
        end_date = datetime.datetime(
            year=2006, month=12, day=31, tzinfo=pytz.utc)

        self.sim_params = SimulationParameters(
            period_start=start_date,
            period_end=end_date
        )

        # portfolio value = 200, 100, 180, 210.6, 421.2, 379.8, 208.494
        returns = pd.Series([1.0, -0.5, 0.8, .17, 1.0, -0.1, -0.45])
        pnl = pd.Series([0, -100, 80, 20.6, 220.6, -41.4, -171.306])

        # the following do not need to be tested as they are provided
        # by zipline
        returns_period = pd.Series()
        max_drawdown = pd.Series()

        return pd.DataFrame({'returns': returns, 'pnl': pnl,
                             'algorithm_period_return': returns_period,
                             'max_drawdown': max_drawdown})
