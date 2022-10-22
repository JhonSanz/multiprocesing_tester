import time
import MetaTrader5 as mt5
import pandas as pd
from get_data import DataGetter
from var import CONFIGURATION, BASE_REQUEST
from .orders import Operation

BUY = 0
SELL = 1

class TwoMeansStrategy:
    def __init__(self, data_getter: DataGetter):
        self.data_getter = data_getter
        self.last_operation = {}

    def run_tick(self):
        order_handler = Operation()
