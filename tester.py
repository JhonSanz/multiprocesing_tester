from itertools import product
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import cpu_count
from main import run_strategy
import numpy as np

INDICATORS = [
    {
        "function": "sma",
        "params": {
            "length": [i for i in range(500, 1001)]
        }, 
        "config_params": {
            "close": "high"
        }
    },
    {
        "function": "sma",
        "params": {
            "length": [i for i in range(500, 1001)]
        }, 
        "config_params": {
            "close": "low"
        }
    },
]

CORES = cpu_count()

STRATEGY_PARAMS = {
    "file": "strategies.two_means.two_sma",
    "params": {
        "data_file": "us100/NAS100_M10_201707030100_202209292350.csv",
        "decimals": 1,
        "deposit": 10000,
        "volume": 0.1,
        "contract_size": 1
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
        executor.submit(Tester(INDICATORS, STRATEGY_PARAMS).run(1, splitted[0]))
        executor.submit(Tester(INDICATORS, STRATEGY_PARAMS).run(2, splitted[1]))
        executor.submit(Tester(INDICATORS, STRATEGY_PARAMS).run(3, splitted[2]))
        executor.submit(Tester(INDICATORS, STRATEGY_PARAMS).run(4, splitted[3]))
