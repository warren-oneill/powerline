from zipline.algorithm import TradingAlgorithm
from zipline.api import order_target, symbol
from zipline.finance.commission import PerShare
from zipline.utils.factory import create_simulation_parameters
from zipline.finance import trading
from zipline.finance.trading import TradingEnvironment

from powerline.utils.data.data_generator import DataGeneratorEpex
from powerline.assets.epex_metadata import MetadataFromSql
from powerline.utils import tradingcalendar_epex as calendar
from powerline.data.loader_power import load_market_data as load


from datetime import timedelta

trading.environment = TradingEnvironment(bm_symbol='^EPEX',
                                  exchange_tz="Europe/Berlin",
                                  env_trading_calendar=calendar,
                                  load=load)
#trading.environment.update_asset_finder(asset_metadata=amd)

dg = DataGeneratorEpex()
_, df = dg.create_data()
start = df.index[0]
end = df.index[-1]

amd = MetadataFromSql()

sid = dg.sid
ident = dg.ident


def initialize(self):
    self.i = 0
    self.set_commission(PerShare(0))


def handle_data(self, data):
    if self.i < 1:
        order_target(symbol(ident), 1)
    self.i += 1

sim_params = create_simulation_parameters(start=start,
                                          end=end)
                                          #data_frequency='minute')
algo = TradingAlgorithm(initialize=initialize,
                        handle_data=handle_data,
                        asset_metadata=amd,
                        sim_params=sim_params,
                        instant_fill=True)
