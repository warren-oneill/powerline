from zipline.history.history_container import HistoryContainer
import pandas as pd
from six import itervalues

from powerline.exchanges.epex_exchange import EpexExchange

__author__ = 'Warren, Max'


class EpexHistoryContainer(HistoryContainer):

    def __init__(self,
                 history_specs,
                 initial_sids,
                 initial_dt,
                 data_frequency,
                 env,
                 bar_data=None):
        super(EpexHistoryContainer, self).__init__(
            history_specs, None, initial_dt, data_frequency, env, bar_data)

        self.length = [spec.bar_count for spec in itervalues(
            self.history_specs)][0]

        products = EpexExchange().products

        self.rolling_frame = {'epex_auction': pd.DataFrame(
            columns=products['hour']),
            'intraday': pd.DataFrame(columns=products['qh']),
            'intraday_h': pd.DataFrame(columns=products['hour'])}

        self.ignored_data = ['cascade', 'auction_signal']

    def frame_from_bardata(self, data, algo_dt):
        """Create a DataFrame from the given BarData and algo dt."""
        data = data._data
        frame_data = {}

        for sid in data:
            event = data[sid]
            if algo_dt != event['dt']:
                continue

            market = event['market']
            if market in self.ignored_data:
                continue

            day = event['day']
            product = event['product']

            if product != '02-03b':
                try:
                    # First naively try to add the data
                    frame_data[market][day].update({product: event['price']})
                except KeyError:
                    try:
                        # Now try as if the market is already seen
                        frame_data[market].update(
                            {day: {product: event['price']}})
                    except KeyError:
                        # If not even the market already exists, create it
                        frame_data.update({market: {day: {product: event[
                            'price']}}})

        if not frame_data:
            return None

        frame = {}
        for market in frame_data.keys():
            # Create pandas DataFrames for the individual markets
            frame.update({market: pd.DataFrame.from_dict(frame_data[market],
                                                         'index')})
            # TODO for continuous intrady this needs to be a Panel
        return frame

    def update(self, data, algo_dt):
        """
        Takes the bar at @algo_dt's f@data, checks to see if we need to roll
        any new digests, then adds new data to the buffer panel.
        """
        frame = self.frame_from_bardata(data, algo_dt)
        self.add_frame(frame)

    def add_frame(self, frame, env=None):
        if frame is None:
            return
        for id in frame.keys():
            current_df = self.rolling_frame[id]
            new_df = frame[id]

            if len(new_df.index) == 1:
                if new_df.index[0] in current_df.index:
                    current_df.update(new_df)
                else:
                    current_df = current_df.append(new_df)
            else:
                # If more than one line is added to the internal data we have
                # to separate the data into already observed and entirely new
                # dates.
                current_dates = current_df.index
                new_dates = new_df.index

                try:
                    update_dates = new_dates.intersection(current_dates)
                    append_dates = new_dates.difference(update_dates)

                    current_df.update(new_df.ix[update_dates])
                    current_df = current_df.append(new_df.ix[append_dates])
                except ValueError:
                    current_df = current_df.append(new_df)

            current_df = current_df.sort()
            if len(current_df) > self.length:
                current_df = current_df.ix[-self.length:]

            self.rolling_frame[id] = current_df

    def get_history(self, history_spec=None, algo_dt=None):
        """
        Main API used by the algoscript is mapped to this function.
        """
        return self.rolling_frame
