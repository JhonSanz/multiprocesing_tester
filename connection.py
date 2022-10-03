import MetaTrader5 as mt5
from termcolor import colored
from var import CREDENTIALS

class Login:
    def __init__(self, credentials):
        self.credentials = credentials

    def login(self):
        if not mt5.initialize():
            print(colored("initialize() failed", "red"))
            mt5.shutdown()
        login = mt5.login(**self.credentials)
        if not login:
            raise Exception(colored("login failed", "red"))
        return mt5.account_info()._asdict()
