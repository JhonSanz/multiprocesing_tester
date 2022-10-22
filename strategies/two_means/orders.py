import MetaTrader5 as mt5
from var import CONFIGURATION


class Operation:
    def __init__(self, request):
        self.request = request

    def sell(self, price, brick_size):
        return

    def buy(self, price, brick_size):
        return
