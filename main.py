from connection import Login
from var import CREDENTIALS
from program import Program
from get_data import DataGetter

INDICATORS = [
    {
        "function": "sma",
        "params": {
            "length": 11
        }
    },
]

login_data = Login(CREDENTIALS).login()
data_getter = DataGetter()
program = Program(INDICATORS, data_getter)
program.run()

