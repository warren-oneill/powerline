__author__ = 'warren'

from unittest import TestCase
import numpy as np
import pandas as pd
from datetime import timedelta
import json

from zipline.utils.factory import create_simulation_parameters
from zipline.finance.commission import PerShare

from gg.powerline.test_algorithms import TestFekAlgo
from gg.powerline.exchanges.epex_exchange import EpexExchange
from gg.powerline.utils.data.data_generator import DataGeneratorEpex
from gg.powerline.prognosis.prog_performance import PrognosisPerformance
# TODO reduce copied code -> add to setUp


class TestFek(TestCase):
    """
    Tests the calculation of the prognosis error
    """
    @classmethod
    def setUpClass(cls):
        products = {'hour': {'2015-06-01': ['01-02']}}
        exchange = EpexExchange()
        env = exchange.env
        ident = '2015-06-01_01-02'
        expiration_date = pd.Timestamp('2015-06-01 00:30',
                                       tz='Europe/Berlin').tz_convert('UTC')
        # TODO relocate to factory
        asset_metadata = {0: {
            'asset_type': 'future', 'symbol': ident, 'expiration_date':
            expiration_date, 'contract_multiplier': 1,
            'children': json.dumps(['CHILD1', 'CHILD2', 'CHILD3', 'CHILD4']),
            'end_date': expiration_date},
            1: {
                'asset_type': 'future', 'symbol': 'CHILD1', 'expiration_date':
                expiration_date, 'end_date': expiration_date +
                timedelta(minutes=30),
                'contract_multiplier': 0.25},
            2: {
                'asset_type': 'future', 'symbol': 'CHILD2', 'expiration_date':
                expiration_date + timedelta(minutes=15),
                'end_date': expiration_date + timedelta(minutes=45),
                'contract_multiplier': 0.25},
            3: {
                'asset_type': 'future', 'symbol': 'CHILD3', 'expiration_date':
                expiration_date + timedelta(minutes=30),
                'end_date': expiration_date + timedelta(minutes=60),
                'contract_multiplier': 0.25},
            4: {
                'asset_type': 'future', 'symbol': 'CHILD4', 'expiration_date':
                expiration_date + timedelta(minutes=45),
                'end_date': expiration_date + timedelta(minutes=75),
                'contract_multiplier': 0.25}}

        env.write_data(futures_data=asset_metadata)
        sid = \
            env.asset_finder.lookup_future_symbol(ident).sid

        cls.data, cls.pnl = DataGeneratorEpex(identifier=ident, env=env
                                              ).create_data()

        sim_params = create_simulation_parameters(start=cls.data.start,
                                                  end=cls.data.end)

        amounts = np.full(25, 1)  # order 1MW for every hour
        cls.algo = TestFekAlgo(
            env=env, sid=sid, amount=amounts, order_count=1,
            instant_fill=False, sim_params=sim_params, commission=PerShare(0),
            data_frequency='minute', day=expiration_date, products=products)

        cls.results = cls.algo.run(cls.data)
        cls.perf = PrognosisPerformance(cls.algo.prog)

        cls.expected_generation = 4*np.array([103.53, 107.89, 108.19, 107.69])
        cls.expected_prog_intraday = 4*np.array([109.325, 107.075, 103.225,
                                                 104.4])

    def test_prog(self):
        for amount in self.algo.prog.values:
            self.assertEqual(amount, 1)

    def test_performance(self):
        self.assertTrue(self.perf.generation.index.equals(
            self.perf.index))
        self.assertTrue(self.perf.prognosis_intraday.index.equals(
                        self.perf.index))

        for i, amount in enumerate(self.expected_generation):
            self.assertAlmostEqual(amount,
                                   self.perf.generation.values[i][0],
                                   delta=2)

        for i, amount in enumerate(self.expected_prog_intraday):
            self.assertEqual(amount, self.perf.prognosis_intraday.values[i][0])

    def test_mape(self):
        test_data = np.array([1, 2, 3, 4]) + np.array(
            self.perf.prognosis_intraday).transpose()[0]
        generation = np.array(self.perf.generation).transpose()[0]

        expected_mape = np.mean(np.abs((generation -
                                        test_data)/generation))

        test_df = pd.DataFrame(test_data, index=self.perf.index, columns=[
            'mw'])
        self.assertEqual(expected_mape, self.perf.mape(test_df))

    def test_rmse(self):
        test_data = np.array([1, 2, 3, 4]) + np.array(
            self.perf.prognosis_intraday).transpose()[0]
        generation = np.array(self.perf.generation).transpose()[0]

        expected_rmse = np.sqrt(np.mean(np.square(
            generation - test_data)))

        test_df = pd.DataFrame(test_data, index=self.perf.index, columns=[
            'mw'])
        self.assertEqual(expected_rmse, self.perf.rmse(test_df))

    def test_ape(self):
        test_data = np.array([1, 2, 3, 4]) + np.array(
            self.perf.prognosis_intraday).transpose()[0]
        generation = np.array(self.perf.generation).transpose()[0]

        expected_ape = np.sum(np.abs(generation - test_data))/(
            np.sum(np.abs(generation)))

        test_df = pd.DataFrame(test_data, index=self.perf.index, columns=[
            'mw'])
        self.assertEqual(expected_ape, self.perf.ape(test_df))

    def test_mean_ramp(self):
        test_data = np.array([1, 2, 3, 4]) + np.array(
            self.perf.prognosis_intraday).transpose()[0]
        expected_mean_ramp = np.mean(np.abs(test_data[0:3] - test_data[1:4]))

        test_df = pd.DataFrame(test_data, index=self.perf.index, columns=[
            'mw'])
        self.assertEqual(expected_mean_ramp, self.perf.mean_ramp(test_df))

    def test_report(self):
        self.perf.display_report()
