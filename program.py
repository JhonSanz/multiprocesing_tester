import concurrent.futures
import threading
from algorithm import AlgorithmSelector
from get_data import DataGetter

class Program:
    def __init__(self, indicators: list, data_getter: DataGetter, max_candles=0):
        self.data_getter = data_getter
        self.indicators = indicators
        self.max_candles = max_candles
        self._data = None
        self.threads = []

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

    def initial_data(self):
        """ It gets data from MT5 as initial data.
            We want it to calculate the given indicators
        """
        self._data = self.data_getter.read_data(self.max_candles)

    def proccess_ia(self):
        return "I am the IA function"

    def proccess_indicators(self):
        aux_data = self._data.copy()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(
                lambda item: AlgorithmSelector(
                    self.data, item["function"], item["params"]
                ).select_algorithm(),
                self.indicators
            )
            for result in results:
                aux_data = aux_data.join(result)
            return aux_data

    def create_proccesses(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            proccess_ia = executor.submit(self.proccess_ia)
            proccess_indicators = executor.submit(self.proccess_indicators)
            print(proccess_ia.result())
            self._data = proccess_indicators.result()
            print(self._data)
 
    def run(self):
        self.get_max_candles_count()
        self.initial_data()
        self.create_proccesses()
        print("aqui estoy")
        # print(self.data)
