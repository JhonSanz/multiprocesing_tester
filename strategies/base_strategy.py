import pandas as pd

class BaseStrategy:
    BUY = 0
    SELL = 1
    _IN = "in"
    _OUT = "out"

    def __init__(self):
        self.orders = []
    
    def open_operation(self, price, date, type, stop_loss=None):
        # print("open position")
        self.orders.append({
            "price_open": price, "date_open": date, "type": type,
            "date_close": None, "price_close": None, "direction": self._IN,
            "stop_loss": stop_loss, "comment": ""
        })
        return len(self.orders) - 1

    def close_operation(self, date_opened, date_close, price_close, comment=""):
        # print("close position")
        # if comment != "":
        #     print("Stop loss")
        position = list(filter(
            lambda x: (
                x["date_open"] == date_opened and
                x["date_close"] is None and
                x["price_close"] is None
            ), self.orders
        ))
        if len(position) == 0:
            return
        position = position[0]
        item_pos = self.orders.index(position)
        position = {
            **position, "date_close": date_close,
            "price_close": price_close,
            "direction": self._OUT,
            "comment": comment
        }
        self.orders[item_pos] = position
    
    def stop_reasons(self, position, high, low):
        return (
            position["stop_loss"] >= low if position["type"] == self.BUY else
            position["stop_loss"] <= high
        )

    def validate_stop_losses(self, current_date, high, low):
        orders = list(filter(
            lambda x: (
                x["direction"] == self._IN and
                x["stop_loss"] is not None and
                x["price_close"] is None and
                x["date_close"] is None and
                self.stop_reasons(x, high, low)
            ), self.orders
        ))
        for operation in orders:
            self.close_operation(
                operation["date_open"], current_date, 
                operation['stop_loss'],
                f"Stop loss at {operation['stop_loss']}"
            )

    def get_position_by_ticket(self, ticket):
        return self.orders[ticket]

    def save_orders(self, filename):
        df = pd.DataFrame(data=self.orders)
        df = df.drop("direction", axis=1)
        # df.to_csv(f"orders/{filename}_orders.csv")
        return df
