import pandas as pd

class BaseStrategy:
    BUY = 0
    SELL = 1
    _IN = "in"
    _OUT = "out"

    def __init__(self):
        self.orders = []
    
    def open_operation(self, price, date, type):
        self.orders.append({
            "price_open": price, "date_open": date, "type": type,
            "date_close": None, "price_close": None, "direction": self._IN
        })

    def close_operation(self, date_opened, date_close, price_close):
        position = list(filter(
            lambda x: x["date_open"] == date_opened, self.orders))[0]
        item_pos = self.orders.index(position)
        position = {
            **position, "date_close": date_close,
            "price_close": price_close,
            "direction": self._OUT
        }
        self.orders[item_pos] = position
    
    def save_orders(self):
        df = pd.DataFrame(data=self.orders)
        df.to_csv("orders.csv")
