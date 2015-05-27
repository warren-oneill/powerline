from zipline.api import order_target, symbol
from zipline.finance.commission import PerShare

from powerline.assets.epex_metadata import MetadataFromSql
from powerline.utils.data.data_generator import DataGeneratorEpex

asset_finder = MetadataFromSql().asset_finder


dg = DataGeneratorEpex()
_, df = dg.create_data()

sid = dg.sid
ident = dg.ident


def initialize(self):
    self.i = 0
    self.set_commission(PerShare(0))


def handle_data(self, data):
    if self.i < 1:
        order_target(symbol(ident), 1)
    self.i += 1
