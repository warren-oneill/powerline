import pandas as pd


__author__ = 'Stefan Hackmann'


def variation_margins_and_costs(results, multiplier):
    '''
    This method calculates variation margins and costs provided that each
    contract has the same multiplier, i.e. position size in MWh.
    Let's get rid of this workaround as soon as zipline's pnl calculation has
    been fixed.
    :param results: zipline results object
    :param multiplier: position size of traded contracts
    :return: variation margin and cost time series
    '''
    # positions = results.positions
    transactions = results.transactions
    index = results.positions.index
    variation_margins = pd.TimeSeries(index=index).fillna(0)
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
            if tra["amount"] > 0:
                prices[tra["sid"]][ts] = tra["price"] \
                                         - tra["commission"]/tra["amount"]
            else:
                prices[tra["sid"]][ts] = tra["price"] \
                                         + tra["commission"]/abs(tra["amount"])
        pass
    return variation_margins, costs
