from connection import Login
from var import CREDENTIALS
from program import Program
from get_data import DataGetter
from strategy import Strategy
from programv2 import ProgramV2

INDICATORS = [
    {
        "function": "renko",
        "params": {
            "custom": True,
            "brick_size": 1
        }
    },
]

STRATEGY_PARAMS = {
    "file": "candles",
    "params": {}
}

if __name__ == '__main__':
    login_data = Login(CREDENTIALS).login()
    data_getter = DataGetter()
    # strategy = Strategy(STRATEGY_PARAMS)
    # module = strategy.validate_strategy_file()
    # strategy.module = module
    # program = Program(
    #     INDICATORS, data_getter, strategy, max_candles=20
    # )
    # program.run_tick()
    program = ProgramV2(data_getter).run_tick()

