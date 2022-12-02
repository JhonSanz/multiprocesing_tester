from itertools import product
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from main import run_strategy
import numpy as np
from strategies.configs import CONFIGS

INDICATORS = [
    {
        "function": "sma",
        "params": {
            "length": [i for i in range(500, 501)]
        }, 
        "config_params": {
            "close": "high"
        }
    },
    {
        "function": "sma",
        "params": {
            "length": [i for i in range(500, 501)]
        }, 
        "config_params": {
            "close": "low"
        }
    },
]

CORES = cpu_count()

STRATEGY_PARAMS = {
    "file": "two_means.dynamic_stop",
    "params": {
        "data_file": "us100/NAS100_M10_201707030100_202209292350.csv",
        **CONFIGS["us100"]
        # "data_file": "eurusd/EURUSD_M10_201707010000_202209300000.csv",
        # **CONFIGS["eurusd"]
    }
}

class Tester:
    def __init__(self, indicators, strategy_params):
        self.indicators = indicators
        self.strategy_params = strategy_params
    
    def run(self, core, _one_to_one):
        try:
            df = pd.read_csv(f"results_core{core}.csv")
        except FileNotFoundError:
            df = None
        last_row = len(df.iloc[:]) if df is not None else 0

        for item in _one_to_one[last_row:]:
            data = run_strategy(item, self.indicators, self.strategy_params)
            if df is None:
                df = pd.DataFrame({
                    "profit": [data],
                    "params": '_'.join(map(str, item))
                })
            else:
                df.loc[len(df)] = {"profit": data, "params": '_'.join(map(str, item))}
            df.to_csv(f"results_core{core}.csv", index=False)


if __name__ == '__main__':
    product_values = list(map(lambda x: x["params"]["length"], INDICATORS))
    """------------------------------------------------------------ """
    """     Define the combination of your indicators' values.      """
    """------------------------------------------------------------ """
    # _product = list(product(*product_values))
    _one_to_one = list(zip(product_values[0], product_values[1]))
    """------------------------------------------------------------ """
    splitted = np.array_split(_one_to_one, CORES)
    with ProcessPoolExecutor(max_workers=CORES) as executor:
        proccessor = [
            executor.submit(Tester(INDICATORS, STRATEGY_PARAMS).run, index, fragment)
            for index, fragment in enumerate(splitted)
            if len(fragment) > 0
        ]
        for future in proccessor:
            future.result()
