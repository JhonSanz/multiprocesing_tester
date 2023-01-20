from get_data import DataGetter
from indicators import Indicators
from strategy_selector import StrategySelector
from generate_statistics import GenerateStatistics
from termcolor import colored
from pips import Pips
from cut_data import cut_data

def run_strategy(config_value, indicators_params, strategy_params):
    print(colored(f"Preparando data para {'_'.join(map(str, config_value))}", "green"))
    data_getter = DataGetter(strategy_params)
    print(colored("Calculando indicadores", "yellow"))
    data_indicators = Indicators(
        config_value,
        indicators_params,
        data_getter.data
    ).choose_algorithms()
    # print("Spreads", sorted(data_indicators["spread"].unique()))
    data_indicators_slice = cut_data(data_indicators, strategy_params, config_value)
    print(colored("Calculando estrategia", "yellow"))
    orders = StrategySelector(
        strategy_params["file"], data_indicators_slice,
        strategy_params["params"]["decimals"]
    ).run_strategy()
    orders.dropna(inplace=True)
    result = GenerateStatistics(orders, config_value, strategy_params).run()
    return result["total"].sum() + strategy_params["params"]["deposit"]
