from unittest import TestCase

from powerline.utils.algos.phelix_algo import algo as algo_eex
from powerline.utils.data.data_generator import DataGeneratorEex
from powerline.exchanges.exchange import EexExchange

from zipline.finance import trading
from zipline.finance.trading import TradingEnvironment

from datetime import timedelta


class TestEexAlgo(TestCase):
    def setUp(self):
        trading.environment = TradingEnvironment(
            bm_symbol='^EEX',
            exchange_tz='Europe/Berlin',
            env_trading_calendar=EexExchange.calendar,
            load=EexExchange.load)
        trading.environment.update_asset_finder(
            asset_finder=EexExchange.asset_finder)
        self.algo = algo_eex
        self.data, self.pnl = DataGeneratorEex().create_data()

    def run_algo(self):
        results = self.algo.run(self.data)
        return results

    def test_algo(self):
        results_algo = self.run_algo()

        for dt, pnl in self.pnl.iterrows():
            # pnl timestamps are at market close
            dt += timedelta(hours=17)

            self.assertEqual(results_algo.pnl[dt], pnl[0])

    def tearDown(self):
        self.algo = None
        trading.environment = None
