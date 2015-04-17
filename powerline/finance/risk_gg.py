from scipy.stats import norm
import numpy as np


class RiskReport(object):
    def __init__(self, perf):
        self.returns = perf.returns
        self.profit = perf.pnl.cumsum().iget(-1)
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