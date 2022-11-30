from get_data import DataGetter
from indicators import Indicators
from strategy_selector import StrategySelector
from statistics import Statistics
from termcolor import colored
from pips import Pips

def run_strategy(config_value, indicators_params, strategy_params):
    print(colored(f"Preparando data para {'_'.join(map(str, config_value))}", "green"))
    data_getter = DataGetter(strategy_params)
    print(colored("Calculando indicadores", "yellow"))
    data_indicators = Indicators(
        config_value,
        indicators_params,
        data_getter.data
    ).choose_algorithms()
    print("Spreads", sorted(data_indicators["spread"].unique()))
    print(colored("Calculando estrategia", "yellow"))
    orders = StrategySelector(
        strategy_params["file"], data_indicators,
        strategy_params["params"]["decimals"]
    ).run_strategy()
    orders.dropna(inplace=True)
    result = Statistics(orders, config_value, strategy_params).run()
    return result["total"].sum() + strategy_params["params"]["deposit"]
