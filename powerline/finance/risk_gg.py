from scipy.stats import norm


class RiskReport(object):
    def __init__(self, perf):
        self.returns = perf.returns
        self.profit = perf.pnl.cumsum().iget(-1)
        self.var_95 = 0
        self.var_99 = 0
        self.calculate_metrics()

    def calculate_metrics(self):
        self.var_95 = self.calculate_var(c=0.95)
        self.var_99 = self.calculate_var(c=0.99)

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
