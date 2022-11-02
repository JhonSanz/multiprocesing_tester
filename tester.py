from itertools import product
import pandas as pd
from main import run_strategy

INDICATORS = [
    {
        "function": "sma",
        "params": {
            "length": [i for i in range(2, 500)]
        }, 
        "config_params": {
            "close": "high"
        }
    },
    {
        "function": "sma",
        "params": {
            "length": [i for i in range(2, 500)]
        }, 
        "config_params": {
            "close": "low"
        }
    },
]

STRATEGY_PARAMS = {
    "file": "strategies.two_means.two_sma",
    "params": {
        "data_file": "us100/NAS100_M10_201701030100_202209292350.csv",
        "decimals": 10**-(1)
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

        """     Define the combination of your indicators' values.      """
        """------------------------------------------------------------ """
        # _product = list(product(*product_values))
        _one_to_one = list(zip(product_values[0], product_values[1]))
        """------------------------------------------------------------ """

        for item in _one_to_one[last_row:]:
            data = run_strategy(item, self.indicators, self.strategy_params)
            if df is None:
                df = pd.DataFrame({
                    "profit": [data],
                    "params": '_'.join(map(str, item))
                })
            else:
                df.loc[len(df)] = {"profit": data, "params": '_'.join(map(str, item))}
            df.to_csv("results.csv", index=False)

Tester(INDICATORS, STRATEGY_PARAMS).run()
