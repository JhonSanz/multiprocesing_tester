import pandas as pd
from main import run_strategy

INDICATORS = [
    {
        "function": "sma",
        "params": {
            "length": [i for i in range(1, 10001)]
        }
    },
]

STRATEGY_PARAMS = {
    "file": "strategies.two_means.two_sma",
    "params": {
        "data_file": "us100/M30"
    }
}

class Tester:
    def __init__(self):
        self.indicators = INDICATORS
        self.stratey_params = STRATEGY_PARAMS
    
    def run(self):
        try:
            df = pd.read_csv("results.csv")
        except FileNotFoundError:
            df = None
        last_row = len(df.iloc[:]) if df else 0
        for item in self.indicators["params"]["length"][last_row:]:
            data = run_strategy(item, self.stratey_params)
            if df == None:
                df = pd.DataFrame({
                    "profit": [data]
                })
            else:
                new_row = pd.Series(data=data, index=["profit"])
                df.append(new_row, ignore_index=True)
            df.to_csv("results.csv")
