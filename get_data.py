import pytz
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from var import CONFIGURATION

class DataGetter:
    def __init__(self, strategy_params):
        self.strategy_params = strategy_params
        self.data = None
        self.get_initial_data()

    def get_initial_data(self):
        self.data = pd.read_csv(f"data/{self.strategy_params['params']['data_file']}", sep='\t')
        self.data['<DATE>'] = self.data['<DATE>'] + ' ' + self.data['<TIME>']
        self.data.rename(columns={
            "<DATE>": "date",
            "<OPEN>": "open",
            "<HIGH>": "high",
            "<LOW>": "low",
            "<CLOSE>": "close",
        }, inplace=True)
        self.data = self.data[['date', 'open', 'high', 'low', 'close']]
        self.data.reset_index(drop=True, inplace=True)
        self.data.reset_index(inplace=True)
        self.data['date'] = pd.to_datetime(self.data['date'], format='%Y.%m.%d')

    def read_data_file(self):
        return
    
    def read_tick_file(self):
        return
