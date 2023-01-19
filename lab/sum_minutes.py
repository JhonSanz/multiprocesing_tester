import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv("totals/4000_4000_10_totals.csv", index_col=[0])
df['date_open'] = pd.to_datetime(df['date_open'], format='%Y-%m-%d %H:%M')
df['date_open'] = df['date_open'] + timedelta(minutes=1)
df['date_open'] = df['date_open'].dt.strftime('%Y.%m.%d %H:%M:%S')

df['date_close'] = pd.to_datetime(df['date_close'], format='%Y-%m-%d %H:%M:%S')
df['date_close'] = df['date_close'] + timedelta(minutes=1)
df['date_close'] = df['date_close'].dt.strftime('%Y.%m.%d %H:%M:%S')
df.to_csv("test.csv")