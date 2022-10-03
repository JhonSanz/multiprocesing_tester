import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import pytz

timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2022, 10, 3, tzinfo=timezone)
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M30, utc_from, 10)
mt5.shutdown()

rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
print(rates_frame)