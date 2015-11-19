from zipline.algorithm import TradingAlgorithm
from zipline.utils.api_support import api_method
from zipline.utils.events import StatelessRule, _build_offset

from gg.powerline.utils.tradingcalendar_epex import get_auctions
from gg.powerline.assets.epex_metadata import EpexMetadata as emd

from gg.database.store import Store
from gg.powerline.mysql_conf import mysql_connection as connection

from datetime import timedelta
import pandas as pd


class TradingAlgorithmAuction(TradingAlgorithm):

    @api_method
    def order_auction(self, amounts, day):
        for i, product in enumerate(self.products['hour'][str(day)]):
            ident = emd.insert_ident(day, product)
            self.order(self.future_symbol(ident), amounts[i])

    def prog_update(self, data):
        for id in data:
            if data[id].market != 'aepp' or id not in \
                    self.perf_tracker.position_tracker.positions.keys():
                continue
            amount = self.perf_tracker.position_tracker.positions[id].amount
            end_ts = self.trading_environment.asset_finder.\
                retrieve_asset(id).end_date
            frame = pd.DataFrame([amount], [end_ts])
            if end_ts in self.prog.index:
                self.prog.update(frame)
            else:
                self.prog = self.prog.append(frame)

    @api_method
    def prognosis(self, sid, as_of):
        end_ts = self.trading_environment.asset_finder.retrieve_asset(
            sid).end_date
        store = Store(connection(), create_new_engine=True)
        session = store.session

        prog = session.execute(
            'select sum(y.VAL) from '
            'PROGNOSIS_INTRADAY as y '
            'JOIN (select *, max(EVENT_TS) as dt from PROGNOSIS_INTRADAY '
            'where BEGIN_TS = "' + str(end_ts) + '" '
            'and EVENT_TS <= "' + str(as_of) + '" '
            'group by BEGIN_TS) '
            'as x on y.EVENT_TS=x.dt and y.BEGIN_TS=x.BEGIN_TS where '
            'y.KIND not like "TS%" '
            'and y.KIND<>"OFFSHORE" '
            'group by y.BEGIN_TS'
            ).fetchall()
        store.finalize()

        return float(prog[0][0])


def auction(algo, data):
    """
    Calculates the current day and then places an auction order for the
    following day.
    """
    day = algo.get_datetime().date() + timedelta(days=1)

    algo.order_auction(day=day, amounts=algo.amount)


class BeforeEpexAuction(StatelessRule):
    """
    A rule that triggers for some offset before the auction.
    Example that triggers triggers before 30 minutes of the auction close:

    BeforeEpexAuction(minutes=30)
    """

    def __init__(self, offset=None, **kwargs):
        self.offset = _build_offset(
            offset,
            kwargs,
            timedelta(minutes=30),  # Defaults to the first minute.
        )
        self._dt = None

    def should_trigger(self, dt, env):
        return (self._get_auction(dt) - self.offset).time() == dt.time()

    def _get_auction(self, dt):
        self._dt = get_auctions(dt)

        return self._dt
