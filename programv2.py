import time
import MetaTrader5 as mt5
import pandas as pd
from get_data import DataGetter
from var import CONFIGURATION, BASE_REQUEST
from orders import Operation

BUY = 0
SELL = 1

class ProgramV2:
    def __init__(self, data_getter: DataGetter):
        self.data_getter = data_getter
        self.last_operation = {}

    def set_last_operation(self, _open, brick, _type):
        self.last_operation = {
            "open": _open,
            "sl": _open - brick if _type == BUY else _open + brick,
            "tp": _open + brick if _type == BUY else _open - brick,
            "type": _type,
        }

    def open_buy(self, order_handler, price, brick_size, _type):
        order_handler.buy(price, brick_size)
        self.set_last_operation(price, brick_size, _type)

    def open_sell(self, order_handler, price, brick_size, _type):
        order_handler.sell(price, brick_size)
        self.set_last_operation(price, brick_size, _type)

    def run_tick(self):
        starttime = time.time()
        point = mt5.symbol_info(CONFIGURATION["market"]).point
        order_handler = Operation(BASE_REQUEST)
        brick_size = 500 * point
        initial_price = self.data_getter.store_tick()['bid']
        print(f"Initial price {initial_price}")

        first_position = True
        while True:
            tick_data = self.data_getter.store_tick()
            py_time = pd.to_datetime(tick_data["time"], unit='s').to_pydatetime()
            current_price = tick_data["bid"]
            print(f"Precio actual {current_price} - fecha {py_time}")

            if first_position:
                if ((current_price - initial_price) >= brick_size):
                    self.open_buy(order_handler, tick_data["ask"], brick_size, BUY)
                    first_position = False
                elif ((initial_price - current_price) >= brick_size):
                    self.open_sell(order_handler, tick_data["bid"], brick_size, SELL)
                    first_position = False
            else:
                if (
                    self.last_operation.get("type") == BUY and
                    current_price > self.last_operation["tp"]
                ):
                    self.open_buy(order_handler, tick_data["ask"], brick_size, BUY)
                elif (
                    self.last_operation.get("type") == BUY and
                    current_price < self.last_operation["sl"]
                ):
                    self.open_sell(order_handler, current_price, brick_size, SELL)
                if (
                    self.last_operation.get("type") == SELL and
                    current_price < self.last_operation["tp"]
                ):
                    self.open_sell(order_handler, current_price, brick_size, SELL)
                elif (
                    self.last_operation.get("type") == SELL and
                    current_price > self.last_operation["sl"]
                ):
                    self.open_buy(order_handler, tick_data["ask"], brick_size, BUY)
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
