import pandas as pd
import numpy as np

from zipline.history.history import HistorySpec
from zipline.protocol import BarData
from zipline.finance.trading import TradingEnvironment

from gg.powerline.history.history_container import EpexExchange
from gg.powerline.history.history_container import EpexHistoryContainer

start_date = pd.Timestamp('2015-06-25', tz='Europe/Berlin').tz_convert('UTC')
end_date = pd.Timestamp('2015-06-28', tz='Europe/Berlin').tz_convert('UTC')
source_start = start_date - pd.Timedelta(hours=2)
exchange = EpexExchange(start=start_date, end=end_date)
env = exchange.env
asset_metadata = {}
env.write_data(futures_data=asset_metadata)
history_spec = HistorySpec(bar_count=2, frequency='1m', field='price',
			   ffill=False, data_frequency='minute', env=env)
history_specs = {}
history_specs[history_spec.key_str] = history_spec

@profile
def test_the_history():
	container = EpexHistoryContainer(history_specs, None, source_start, 'minute',
					 env=env)

	data = {}
	data[1] = {'dt': pd.Timestamp('2015-06-27'),
		   'price': np.random.uniform(0, 100),
		   'market': 'epex_auction',
		   'product': '00-01',
		   'day': pd.Timestamp('2015-06-27'),
		   'sid': 1}
	data[2] = {'dt': pd.Timestamp('2015-06-26'),
		   'price': np.random.uniform(0, 100),
		   'market': 'epex_auction',
		   'product': '00-01',
		   'day': pd.Timestamp('2015-06-26'),
		   'sid': 2}
	for current_sid in data:
	    current_data = data[current_sid]
	    bar = BarData({current_sid: current_data})
	    container.update(bar, current_data['dt'])

	history = container.get_history()

	print(history['epex_auction'])


if __name__=='__main__':
	test_the_history()
