import threading
from algorithm import AlgorithmSelector
from get_data import DataGetter

class Program:
    def __init__(self, indicators: list, data_getter: DataGetter, max_candles=0):
        self.data_getter = data_getter
        self.indicators = indicators
        self.max_candles = max_candles
        self._data = []
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

    def create_threads(self):
        for item in self.indicators:
            selector = AlgorithmSelector(
                self.data, item["function"], item["params"])
            t = threading.Thread(target=selector.select_algorithm)
            self.threads.append(t)

    def run(self):
        self.get_max_candles_count()
        self.initial_data()
        self.create_threads()

        print(self.data)
        print(self.threads)
