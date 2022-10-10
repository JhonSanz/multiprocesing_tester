import MetaTrader5 as mt5

CREDENTIALS = {
    "login": 64627016,
    "password": "Holajeje123",
    "server": "XMGlobal-MT5 2"
}

CONFIGURATION = {
    "broker_timezone": "Europe/Moscow",
    "market": "US100Cash",
    # "market": "EURUSD",
    "frametime": 1,
    "volume": 0.1
}

BASE_REQUEST = {
    "action": mt5.TRADE_ACTION_DEAL,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
    "symbol": CONFIGURATION["market"],
    "volume": CONFIGURATION["volume"],
    "deviation": 20,
}