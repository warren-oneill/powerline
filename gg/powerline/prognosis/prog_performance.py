import pandas as pd
import numpy as np

from gg.database.store import Store
from gg.database.mysql_conf import mysql_connection_aws as mysql_connection

__author__ = 'Warren'


class ProgPerformance(object):
    def __init__(self, open_mw):
        self.open_mw = open_mw
        self.index = open_mw.index
        self.start = self.index[0]
        self.end = self.index[-1]
        self.sq_error = pd.DataFrame(index=self.index)

        self.store = Store(mysql_connection(), create_new_engine=True)
        self.session = self.store.session

    def prog_error(self):
        prod_id = self.session.execute(
            'select sum(y.VAL) from '
            'PROGNOSIS_INTRADAY as y '
            'JOIN (select *, max(EVENT_TS) as dt from PROGNOSIS_INTRADAY '
            'where BEGIN_TS <= "' + str(self.end) + '" and BEGIN_TS >= "'
            + str(self.start) + '" group by BEGIN_TS order by BEGIN_TS) as x '
            'on y.EVENT_TS=x.dt and y.BEGIN_TS=x.BEGIN_TS where y.KIND not '
            'like "TS%" and y.KIND<>"OFFSHORE" group by y.BEGIN_TS'
           ).fetchall()

        ist = self.session.execute(
            'select sum(VAL) from GG_GENERATION_AGGREGATED where ' \
              'BEGIN_TS <= "' + str(self.end) + '" and BEGIN_TS >= "'
        + str(self.start) +  '" and KIND not like "TS%" and KIND<>"OFFSHORE" '
                             'group by BEGIN_TS order by BEGIN_TS').fetchall()

        return pd.DataFrame(ist, index=self.index) - pd.DataFrame(prod_id,
                                                                  self.index)

