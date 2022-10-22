import pytz
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from var import CONFIGURATION

class DataGetter:
    def __init__(self, max_candles, strategy_params):
        self.max_candles = max_candles
        self.strategy_params = strategy_params
        self.data = None
        self.get_initial_data()

    def get_initial_data(self):
        self.data = pd.read_csv(f"data/{self.strategy_params['data_file']}")

    def read_data_file(self):
        return
    
    def read_tick_file(self):
        return
