from itertools import product
import pandas as pd
from main import run_strategy

INDICATORS = [
    {
        "function": "sma",
        "params": {
            "length": [10, 11] # [i for i in range(1, 5)]
        }, 
        "config_params": {
            "close": "high"
        }
    },
    {
        "function": "sma",
        "params": {
            "length": [12] # [i for i in range(5, 10)]
        }, 
        "config_params": {
            "close": "low"
        }
    },
]

STRATEGY_PARAMS = {
    "file": "strategies.two_means.two_sma",
    "params": {
        "data_file": "us100/M30.csv"
    }
}

class Tester:
    def __init__(self, indicators, strategy_params):
        self.indicators = indicators
        self.strategy_params = strategy_params
    
    def run(self):
        try:
            df = pd.read_csv("results.csv")
        except FileNotFoundError:
            df = None
        last_row = len(df.iloc[:]) if df is not None else 0
        product_values = list(map(lambda x: x["params"]["length"], self.indicators))
        for item in list(product(*product_values))[:]:
            data = run_strategy(item, self.indicators, self.strategy_params)
            if df is None:
                df = pd.DataFrame({
                    "profit": [data]
                })
            else:
                df.loc[len(df)] = {"profit": data}
            # df.to_csv("results.csv", index=False)

Tester(INDICATORS, STRATEGY_PARAMS).run()
