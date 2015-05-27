from unittest import TestCase

from powerline.utils.algos.epex_algo import initialize, handle_data
from powerline.utils.data.data_generator import DataGeneratorEpex
from powerline.assets.epex_metadata import MetadataFromSql
from powerline.utils import tradingcalendar_epex as calendar
from powerline.data.loader_power import load_market_data as load


from zipline.finance import trading
from zipline.finance.trading import TradingEnvironment
from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import create_simulation_parameters


class TestEpexAlgo(TestCase):

    def setUp(self):
        trading.environment = TradingEnvironment(
            bm_symbol='^EPEX',
            exchange_tz="Europe/Berlin",
            env_trading_calendar=calendar,
            load=load
        )

        asset_finder = MetadataFromSql().asset_finder

        trading.environment.update_asset_finder(asset_finder=asset_finder)

        self.data, self.pnl = DataGeneratorEpex().create_data()
        start = self.pnl.index[0]
        end = self.pnl.index[-1]
        sim_params = create_simulation_parameters(start=start,
                                                  end=end)

        self.algo = TradingAlgorithm(
            initialize=initialize,
            handle_data=handle_data,
            asset_finder=asset_finder,
            sim_params=sim_params,
            instant_fill=True
        )

    def run_algo(self):
        print(trading.environment.bm_symbol)
        results = self.algo.run(self.data)
        return results

    def test_algo(self):
        results_algo = self.run_algo()

        for dt, pnl in self.pnl.iterrows():
            # pnl timestamps are at market close

            self.assertEqual(results_algo.pnl[dt], pnl[0])

    def tearDown(self):
        self.algo = None
        trading.environment = None
