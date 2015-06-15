from scipy.stats import norm
import numpy as np
from tabulate import tabulate


class RiskReport(object):
    '''
    Collects all zipline risk parameters and adds gg-specific parameters
    e.g. VaR.
    A report can be displayed in the terminal by calling display_report()
    '''
    def __init__(self, perf):
        self.returns = perf.returns
        self.returns_max = perf.returns.max()
        self.returns_min = perf.returns.min()
        self.returns_period = perf.algorithm_period_return[-1]
        self.profit = perf.pnl.cumsum()[-1]
        self.pnl_max = perf.pnl.max()
        self.pnl_min = perf.pnl.min()
        self.max_drawdown = perf.max_drawdown[-1]
        start = perf.index[0].strftime('%Y-%m-%d')
        end = perf.index[-1].strftime('%Y-%m-%d')
        self.sortino = perf.sortino[-1]
        self.sharpe = perf.sharpe[-1]
        self.information = perf.information[-1]
        self.period = start + ' to ' + end

        self.var_95 = 0
        self.var_99 = 0
        self.win_loss = 0

        self.calculate_metrics()

    def calculate_metrics(self):
        self.var_95 = self.calculate_var(c=0.95)
        self.var_99 = self.calculate_var(c=0.99)
        self.win_loss = self.calculate_win_loss()

    def calculate_var(self, c):
        """
        Variance-Covariance calculation of daily Value-at-Risk
        using confidence level c, with mean of returns mu
        and standard deviation of returns sigma, on a portfolio
        of value P.
        """
        mu = self.returns.mean()
        sigma = self.returns.std()

        alpha = norm.ppf(1-c, mu, sigma)

        return self.profit*(1 - (alpha + 1))

    def calculate_win_loss(self):
        win_loss_count = np.sign(self.returns).value_counts()

        win_loss = np.round(win_loss_count[1]/win_loss_count[-1], 2)

        return win_loss

    def display_report(self):
        table = [
                ["PnL (€)", self.profit],
                ["PnL Tag Max (€)", self.pnl_max],
                ["PnL Tag Min (€)", self.pnl_min],
                ["Returns (%)", self.returns_period],
                ["Returns Tag Max (%)", self.returns_max],
                ["Returns Tag Min (%)", self.returns_min],
                ["Sortino", self.sortino],
                ["Sharpe", self.sharpe],
                ["Information", self.information],
                ["Max Drawdown (%)", self.max_drawdown],
                ["VaR 95 (€)", self.var_95],
                ["VaR 99 (€)", self.var_99],
                ["Win Loss Ratio", self.win_loss]]
        headers = ["Risk Report", self.period]
        print(tabulate(table, headers, tablefmt="fancy_grid",
                       numalign="right"))
