import pandas as pd
import numpy as np
from tabulate import tabulate

from gg.database.store import Store
from gg.powerline.mysql_conf import mysql_connection as connection

__author__ = 'Warren'


class PrognosisPerformance(object):
    def __init__(self, open_mw):
        self.open_mw = open_mw
        self.open_mw.columns = ['mw']
        self.index = open_mw.index
        self.start = self.index[0]
        self.end = self.index[-1]
        start = self.index[0].strftime('%Y-%m-%d')
        end = self.index[-1].strftime('%Y-%m-%d')
        self.period = start + ' to ' + end

        store = Store(connection(), create_new_engine=True)
        self.session = store.session

        self._generation = None
        self._prognosis_intraday = None
        self._strategy_abs_error = None

    def mape(self, df):
        """
        :param df:
        :return:mean percent error
        """
        return (self.generation - df).divide(self.generation).abs().mean()\
            .values[0]

    def rmse(self, df):
        return np.sqrt(((self.generation - df)**2).mean()).values[0]

    @property
    def generation(self):
        if self._generation is None:
            self._generation = self.session.execute(
                'select BEGIN_TS, sum(VAL) from GG_GENERATION_AGGREGATED '
                'where '
                'BEGIN_TS <= "' + str(self.end) + '" and BEGIN_TS >= "'
                + str(self.start) + '" and KIND not like "TS%" '
                'group by BEGIN_TS order by BEGIN_TS'
            ).fetchall()

        return pd.DataFrame(self._generation, columns=['dt', 'mw']).\
            set_index('dt').tz_localize('UTC').astype(float)/4

    @property
    def prognosis_intraday(self):
        if self._prognosis_intraday is None:
            offshore = ''
            if self.start >= pd.Timestamp('2015-06-01', tz='Europe/Berlin').\
                    tz_convert('UTC'):
                    offshore = 'and y.KIND<>"OFFSHORE" '
            self._prognosis_intraday = self.session.execute(
                'select y.BEGIN_TS, sum(y.VAL) from '
                'PROGNOSIS_INTRADAY as y '
                'JOIN (select *, max(EVENT_TS) as dt from PROGNOSIS_INTRADAY '
                'where BEGIN_TS <= "' + str(self.end) + '" and BEGIN_TS >= "'
                + str(self.start) + '" group by BEGIN_TS order by BEGIN_TS) '
                'as x on y.EVENT_TS=x.dt and y.BEGIN_TS=x.BEGIN_TS where '
                'y.KIND not like "TS%" '
                + offshore +
                'group by y.BEGIN_TS'
                ).fetchall()
            self._prognosis_intraday = pd.DataFrame(
                self._prognosis_intraday, columns=['dt', 'mw']).\
                set_index('dt').tz_localize('UTC').astype(float)/4

        return self._prognosis_intraday

    def display_report(self):
        """
        displays ascii table in the terminal
        """
        table = [
                ["Current RMSE", self.rmse(self.prognosis_intraday)],
                ["Current MAPE (%)", self.mape(self.prognosis_intraday)*100],
                ["New RMSE", self.rmse(self.prognosis_intraday+self.open_mw)],
                ["New MAPE (%)", self.mape(
                    self.prognosis_intraday+self.open_mw)*100]]
        headers = ["Prognosis Report", self.period]
        print(tabulate(table, headers, tablefmt="fancy_grid",
                       numalign="right"))
