from get_data import DataGetter
from indicators import Indicators
from strategies.two_means.two_sma import TwoMeansStrategy


def run_strategy(config_value, indicators_params, strategy_params):
    data_getter = DataGetter(strategy_params)
    data_indicators = Indicators(
        config_value,
        indicators_params,
        data_getter.data
    ).choose_algorithms()
    data_indicators.to_csv("test_data_indicators.csv", index=False)
    # program = TwoMeansStrategy(data_indicators).run()
    return 592
