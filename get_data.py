import pytz
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from var import CONFIGURATION

class DataGetter:
    def __init__(self):
        self.data = []

    def read_data(self, max_candles):
        timezone = pytz.timezone("Europe/Moscow")
        utc_from = datetime.now(tz=timezone)
        # timezone = pytz.timezone("Etc/UTC")
        # utc_from = datetime.now()
        # print(utc_from)
        rates = mt5.copy_rates_from(
            "EURUSD", mt5.TIMEFRAME_M30, utc_from,
            max_candles
        )
        rates_frame = pd.DataFrame(rates)
        rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
        return rates_frame

    def store_tick(self):
        tick = mt5.symbol_info_tick(CONFIGURATION["market"])._asdict()
        return tick
