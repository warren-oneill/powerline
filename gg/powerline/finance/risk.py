__author__ = "Warren"

from scipy.stats import norm
import numpy as np
from tabulate import tabulate
import pandas as pd
from pyfolio.timeseries import gen_drawdown_table

number_drawdowns_for_longest = 20


class RiskReport(object):
    """
    Collects all zipline risk parameters and adds gg-specific parameters
    e.g. VaR.
    A report can be displayed in the terminal by calling display_report()
    """

    def __init__(self, perf, sim_params):
        self.returns = perf.returns
        self.returns_max = perf.returns.max()
        self.returns_min = perf.returns.min()
        self.returns_period = perf.algorithm_period_return[-1]
        self.profit = perf.pnl.cumsum()[-1]
        self.pnl_max = perf.pnl.max()
        self.pnl_min = perf.pnl.min()
        self.max_drawdown = perf.max_drawdown[-1]

        self.benchmark = perf.benchmark_period_return
        self.benchmark_profits = perf.benchmark_period_return[-1] * \
            sim_params.capital_base

        self.sortino = perf.sortino[-1]
        self.sharpe = perf.sharpe[-1]
        self.information = perf.information[-1]

        start = sim_params.period_start.strftime('%Y-%m-%d')
        self.end_dt = sim_params.period_end
        self.period = start + ' to ' + self.end_dt.strftime('%Y-%m-%d')

        self.var_95 = 0
        self.var_99 = 0
        self.five_day_var_95 = 0
        self.five_day_var_99 = 0
        self.win_loss = 0
        self.longest_drawdown_duration = pd.Timestamp(0)

        self.calculate_metrics()

    def calculate_metrics(self):
        self.var_95 = self.calculate_var(c=0.95)
        self.var_99 = self.calculate_var(c=0.99)
        self.five_day_var_95 = self.calculate_var(c=0.95, n=5)
        self.five_day_var_99 = self.calculate_var(c=0.99, n=5)
        self.win_loss = self.calculate_win_loss()

        self.longest_drawdown_duration = \
            self.calculate_longest_drawdown_duration()

    def calculate_var(self, c, n=1):
        """
        Variance-Covariance calculation of daily Value-at-Risk based on a
        normal distribution model with mean of returns mu and standard
        deviation of returns sigma, on a portfolio of value P.
        see page 9: https://people.math.ethz.ch/~embrecht/ftp/LongTermRisk.pdf

        :param c: confidence level of the calculation
        :param n: length of the considered time period (multiple of the base
            interval; here generally number of days)
        :return: the value at risk (VaR) over given period n
        """
        mu = self.returns.mean()
        sigma = self.returns.std()
        P = self.profit

        alpha = norm.ppf(1 - c, n*mu, np.sqrt(n)*sigma)

        return - P * alpha

    def calculate_win_loss(self):
        """
        ratio of wins over loses
        """
        win_loss_count = np.sign(self.returns).value_counts()

        win_loss = np.round(win_loss_count[1] / win_loss_count[-1], 2)

        return win_loss

    def calculate_longest_drawdown_duration(self):
        drawdown_table = gen_drawdown_table(self.returns,
                                            top=number_drawdowns_for_longest)
        if pd.isnull(drawdown_table['duration']).any():
            last_peak = np.argmax(self.returns.cumsum())
            if last_peak.tz is None:
                last_peak = last_peak.tz_localize('UTC')

            final_drawdown_duration = len(pd.date_range(last_peak, self.end_dt,
                                                        freq='B'))
            longest_drawdown_duration = max(final_drawdown_duration,
                                            drawdown_table['duration'].max())
        else:
            longest_drawdown_duration = drawdown_table['duration'].max()

        return longest_drawdown_duration

    def display_report(self):
        """
        displays ascii table in the terminal
        """
        table = [
                ["PnL (€)", self.profit],
                ["PnL Tag Max (€)", self.pnl_max],
                ["PnL Tag Min (€)", self.pnl_min],
                ["Returns (%)", self.returns_period*100],
                ["Returns Day Max (%)", self.returns_max*100],
                ["Returns Day Min (%)", self.returns_min*100],
                ["Sortino", self.sortino],
                ["Sharpe", self.sharpe],
                ["Information", self.information],
                ["Max Drawdown (%)", self.max_drawdown*100],
                ["Longest Drawdown Duration*", self.longest_drawdown_duration],
                ["VaR 95 (€)", self.var_95],
                ["VaR 99 (€)", self.var_99],
                ["VaR 95 (€), 5 days", self.five_day_var_95],
                ["VaR 99 (€), 5 days", self.five_day_var_99],
                ["Win Loss Ratio", self.win_loss],
                ["Total Benchmark Profit (€)", self.benchmark_profits]]
        headers = ["Risk Report", self.period]

        pd.concat([self.returns.cumsum(), self.benchmark], axis=1).plot()

        print(tabulate(table, headers, tablefmt="fancy_grid",
                       numalign="right"))

        print("* : " +
              "Among the top %d drawdowns." % number_drawdowns_for_longest)
