import MetaTrader5 as mt5
from var import CONFIGURATION


class Operation:
    def __init__(self, request):
        self.request = request

    def sell(self, price, brick_size):
        self.request["type"] =  mt5.ORDER_TYPE_SELL
        self.request["price"] = price
        self.request["sl"] = price + brick_size
        self.request["tp"] = price - brick_size
        mt5.order_send(self.request)
        # self.print_order_result(price)

    def buy(self, price, brick_size):
        self.request["type"] =  mt5.ORDER_TYPE_BUY
        self.request["price"] = price
        self.request["sl"] = price - brick_size
        self.request["tp"] = price + brick_size
        mt5.order_send(self.request)
        # self.print_order_result(price)

    def print_order_result(self, price):
        result = mt5.order_send(self.request)
        print(
            f"""1. order_send(): by {CONFIGURATION['market']}, {CONFIGURATION['volume']} lots at {price}"""
        )
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"2. order_send failed, retcode={result.retcode}")
            result_dict = result._asdict()
            for field in result_dict.keys():
                print(f"{field}={result_dict[field]}")
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print(f"traderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
