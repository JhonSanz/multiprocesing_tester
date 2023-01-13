from itertools import product
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from main import run_strategy
import numpy as np
from strategies.configs import CONFIGS
from join_files import results_concat
import os
import re
import shutil

INDICATORS = [
    {
        "function": "sma",
        "params": {
            "length": [i for i in range(4000, 4001, 1)]
        }, 
        "config_params": {
            "close": "high"
        }
    },
    {
        "function": "sma",
        "params": {
            "length": [i for i in range(4000, 4001, 1)]
        }, 
        "config_params": {
            "close": "low"
        }
    },
    {
        "function": "atr",
        "params": {
            "length": [i for i in range(10, 11, 1)]
        }, 
        "config_params": {
            "close": "close",
            "high": "high",
            "low": "low",
        }
    }
]

CORES = cpu_count()

STRATEGY_PARAMS = {
    "file": "two_means.two_means_atr_stop_loss",
    "params": {
        "data_file": "us100/NAS100_M1_202101040100_202212232354.csv",
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

def permutations(values):
    _product = list(product(*values))
    result = list(filter(lambda x: x[0] == x[1], _product))
    # _one_to_one = list(zip(product_values[0], product_values[1]))
    return result

if __name__ == '__main__':
    turn_pc_off = input("Apagar pc despues del backtesting? (y/n): ")
    product_values = list(map(lambda x: x["params"]["length"], INDICATORS))
    _permutations = permutations(product_values)

    splitted = np.array_split(_permutations, CORES)
    with ProcessPoolExecutor(max_workers=CORES) as executor:
        proccessor = [
            executor.submit(Tester(INDICATORS, STRATEGY_PARAMS).run, index, fragment)
            for index, fragment in enumerate(splitted)
            if len(fragment) > 0
        ]
        for future in proccessor:
            future.result()
    
    dirs = [x for x in os.listdir("./") if re.compile("test_results_*").search(x) is not None]
    dirs = list(sorted(dirs))
    new_dir = 1
    if not dirs:
        os.makedirs(f"test_results_{new_dir}")
    else:
        new_dir = int(dirs[-1].split('test_results_')[-1]) + 1
        os.makedirs(f"test_results_{new_dir}")
    for file in os.listdir("./"):
        if file.split('.')[-1] == 'csv':
            shutil.move(file, f"test_results_{new_dir}")
    results_concat(f"test_results_{new_dir}", f"test_results_{new_dir}", new_dir)
    if turn_pc_off == "y":
        os.system("shutdown /s /t 1")
