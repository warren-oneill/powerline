from scipy.stats import norm

def var_cov_var(data, capital, c=0.99):
    """
    Variance-Covariance calculation of daily Value-at-Risk
    using confidence level c, with mean of returns mu
    and standard deviation of returns sigma, on a portfolio
    of value P.
    """
    mu = data.mean()
    sigma = data.std()

    alpha = norm.ppf(1-c, mu, sigma)
    return capital - capital*(alpha + 1)