from get_data import DataGetter
from indicators import Indicators
from strategies.two_means.two_sma import TwoMeansStrategy
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
    orders = TwoMeansStrategy(
        data_indicators,
        strategy_params["params"]["decimals"]
    ).run()
    orders.dropna(inplace=True)
    pips_calculatior = Pips(
        strategy_params["params"]["decimals"],
        strategy_params["params"]["volume"],
        strategy_params["params"]["contract_size"],
    )
    result = Statistics(orders, config_value, pips_calculatior).run()
    return result["total"].sum() + strategy_params["params"]["deposit"]
