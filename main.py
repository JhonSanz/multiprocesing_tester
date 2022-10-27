from get_data import DataGetter
from indicators import Indicators
from strategies.two_means.two_sma import TwoMeansStrategy
from statistics import Statistics

def run_strategy(config_value, indicators_params, strategy_params):
    data_getter = DataGetter(strategy_params)
    data_indicators = Indicators(
        config_value,
        indicators_params,
        data_getter.data
    ).choose_algorithms()
    # data_indicators.to_csv("test_data_indicators.csv", index=False)
    orders = TwoMeansStrategy(data_indicators).run()
    orders.dropna(inplace=True)
    result = Statistics(orders, config_value).run()
    return result["total"].sum()
