from connection import Login
from var import CREDENTIALS
from program import Program
from get_data import DataGetter
from indicators import Indicators
from programv2 import ProgramV2
from strategies.two_means.two_sma import TwoMeansStrategy


def run_strategy(config_value, strategy_params):
    # login_data = Login(CREDENTIALS).login()
    data_getter = DataGetter(
        config_value,
        strategy_params
    )
    data_indicators = Indicators(
        config_value,
        data_getter.data
    ).choose_algorithms()
    # program = Program(
    #     INDICATORS, data_getter, strategy, max_candles=20
    # )
    # program.run_tick()
    program = TwoMeansStrategy(data_getter).run_tick()
    return 1
