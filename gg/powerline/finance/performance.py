import pandas as pd


__author__ = 'Stefan Hackmann'


def pnl_and_costs(results, multiplier):
    """
    This method calculates pnl and costs provided that each
    contract has the same multiplier, i.e. position size in MWh.
    TODO Let's get rid of this workaround as soon as zipline's pnl
    calculation has been fixed.
    :param results: zipline results object
    :param multiplier: position size of traded contracts
    :return: pnl ex commission and cost time series
    """
    transactions = results.transactions
    index = results.positions.index
    pnl = pd.TimeSeries(index=index).fillna(0)
    costs = pd.TimeSeries(index=index).fillna(0)
    sids = set()
    for ts in index:
        for pos in results.positions[ts]:
            sids.add(pos["sid"])
    prices = pd.DataFrame(index=index, columns=sids)
    positions = prices.copy().fillna(0)
    for ts in index:
        for pos in results.positions[ts]:
            positions[pos["sid"]][ts] = pos["amount"]
        for tra in transactions[ts]:
            costs[ts] += tra["commission"] * multiplier
            # if tra["amount"] > 0:
            prices[tra["sid"]][ts] = \
                tra["price"] - tra["commission"]/tra["amount"]
            # else:
            #     prices[tra["sid"]][ts] = tra["price"] \
            #         - tra["commission"]/tra["amount"]
    for i in range(1, len(index)):
        for sid in sids:
            pnl[index[i]] += \
                multiplier*positions[sid][index[i-1]] \
                * (prices[sid][index[i]]-prices[sid][index[i-1]])
    return pnl, costs
