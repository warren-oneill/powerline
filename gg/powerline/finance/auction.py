from zipline.algorithm import TradingAlgorithm
from zipline.utils.api_support import api_method


class TradingAlgorithmGG(TradingAlgorithm):
    def insert_idents(self, day, freq):
        if freq == 'H':
            index = 24
        else:
            index = 96

        idents = {}
        for i in range(1, index):
            idents.update({i: str(day) + '_' + freq + str(i)})

        return idents

    @api_method
    def order_auction(self, amounts, day, freq='H'):
        idents = self.insert_idents(day, freq)

        for i in idents:
            self.order(self.symbol(idents[i]), amounts[i])
