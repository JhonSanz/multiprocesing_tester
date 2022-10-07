from connection import Login
from var import CREDENTIALS
from program import Program
from get_data import DataGetter
from strategy import Strategy

INDICATORS = [
    {
        "function": "sma",
        "params": {
            "length": 11
        }
    },
    {
        "function": "rsi",
        "params": {
            "length": 10
        }
    },
    {
        "function": "rsi",
        "params": {
            "length": 9
        }
    },
    {
        "function": "rsi",
        "params": {
            "length": 8
        }
    },
]

STRATEGY_PARAMS = {
    "file": "candles",
    "params": {}
}

if __name__ == '__main__':
    login_data = Login(CREDENTIALS).login()
    data_getter = DataGetter()
    strategy = Strategy(STRATEGY_PARAMS)
    module = strategy.validate_strategy_file()
    strategy.module = module
    program = Program(INDICATORS, data_getter, strategy)
    program.run()
