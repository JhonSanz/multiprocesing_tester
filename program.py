import time
from datetime import datetime, timedelta
import concurrent.futures
import pandas as pd
from algorithm import AlgorithmSelector
from strategy import Strategy
from get_data import DataGetter
from var import CONFIGURATION

class Program:
    def __init__(
        self, indicators: list, data_getter: DataGetter,
        strategy: Strategy, max_candles=0
    ):
        self.data_getter = data_getter
        self.strategy = strategy
        self.indicators = indicators
        self.max_candles = max_candles
        self._data = None
        self.computed_indicators = None
        self.ia_signal = None
        self.last_candle = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def get_max_candles_count(self):
        self.max_candles = sorted(list(
            map(lambda x: x["params"]["length"], self.indicators)
        ), reverse=True)[0]

    def read_data_mt5(self):
        """ It gets data from MT5 as initial data.
            We want it to calculate the given indicators
        """
        data = self.data_getter.read_data(self.max_candles)
        self.last_candle = data.iloc[-1,0].to_pydatetime()
        return data

    def thread_ia(self):
        return "I am the IA function"

    def thread_indicators(self):
        aux_data = self._data.loc[:, ["open", "close"]].copy()
        for item in self.indicators:
            result = AlgorithmSelector(
                    self.data, item["function"], item["params"]
                ).select_algorithm()
            aux_data = aux_data.join(result)
        return aux_data

    """ This code will remain commented out in case I need it in the future """
    # def thread_indicators(self):
    #     return self.test_performace()
    #     aux_data = self._data.loc[:, ["open", "close"]].copy()
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         results = executor.map(
    #             lambda item: AlgorithmSelector(
    #                 self.data, item["function"], item["params"]
    #             ).select_algorithm(),
    #             self.indicators
    #         )
    #         for result in results:
    #             aux_data = aux_data.join(result)
    #         return aux_data

    def create_threads(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread_ia = executor.submit(self.thread_ia)
            thread_indicators = executor.submit(self.thread_indicators)
            self.ia_signal = thread_ia.result()
            self.computed_indicators = thread_indicators.result()

    def check_strategy_entries(self):
        pass
 
    def run(self):
        self.get_max_candles_count()
        self._data = self.read_data_mt5()
        self.computed_indicators = self.thread_indicators()
        starttime = time.time()

        while True:
            tick_data = self.data_getter.store_tick()
            py_time = pd.to_datetime(tick_data["time"], unit='s').to_pydatetime()
            next_candle = self.last_candle + timedelta(
                seconds=CONFIGURATION["frametime"] * 60)
            # print(py_time)
            if (py_time > next_candle): # cuando la vela termina
                self._data = self.read_data_mt5()
                self.create_threads()
                operation = self.strategy.run(
                    self._data, self.computed_indicators,
                    self.ia_signal
                )
                print(operation)

            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
