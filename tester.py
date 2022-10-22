import pandas as pd
from main import run_strategy

INDICATORS = [
    {
        "function": "sma",
        "params": {
            "length": [i for i in range(10, 11)]
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
        last_row =len(df.iloc[:]) if df is not None else 0
        for item in self.indicators[0]["params"]["length"][last_row:]:
            data = run_strategy(item, self.indicators, self.strategy_params)
            if df is None:
                df = pd.DataFrame({
                    "profit": [data]
                })
            else:
                df.loc[len(df)] = {"profit": data}
            df.to_csv("results.csv", index=False)

Tester(INDICATORS, STRATEGY_PARAMS).run()
