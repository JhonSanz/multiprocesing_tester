import pandas as pd
from datetime import datetime

class BaseStrategy:
    BUY = 0
    SELL = 1
    _IN = "in"
    _OUT = "out"

    def __init__(self):
        self.orders = []
        self.opened_position = False

    def open_operation(self, price, date, type, spread, stop_loss=None):
        real_price = 0
        if (type == self.BUY):
            # Opens position in ask
            real_price = price + spread
        elif (type == self.SELL):
            # Opens position in bid
            real_price = price

        self.orders.append({
            "price_open": real_price, "date_open": date, "type": type,
            "date_close": None, "price_close": None, "direction": self._IN,
            "stop_loss": stop_loss, "comment": ""
        })
        return len(self.orders) - 1

    def close_operation(self, date_opened, date_close, price_close, comment=""):
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

    def stop_reasons(self, position, high, low, spread):
        return (
            position["stop_loss"] > low
            if position["type"] == self.BUY else
            position["stop_loss"] < high + spread
        )

    def validate_stop_losses(self, current_date, high, low, spread, price_close=None):
        orders = list(filter(
            lambda x: (
                x["direction"] == self._IN and
                x["stop_loss"] is not None and
                x["price_close"] is None and
                x["date_close"] is None and
                self.stop_reasons(x, high, low, spread)
            ), self.orders
        ))
        for operation in orders:
            self.close_operation(
                operation["date_open"], current_date,
                price_close or operation['stop_loss'],
                f"Stop loss at {price_close or operation['stop_loss']}"
            )
            self.opened_position = False

    def get_position_by_ticket(self, ticket):
        return self.orders[ticket]

    def save_orders(self, filename):
        df = pd.DataFrame(data=self.orders)
        df = df.drop("direction", axis=1)
        # df.to_csv(f"orders/{filename}_orders.csv")
        return df

    def edit_position(self, current_price, spread, position, option, value, current_date):
        options = ["stop_loss", "take_profit"]
        if not option in options:
            raise Exception(f"""
                {option} is not valid a valid option.
                Possible values are: {options}
            """)
        if option == "stop_loss":
            self.validate_invalid_stop(
                current_price, value,
                position, spread, current_date
            )
        item_pos = self.orders.index(position)
        self.orders[item_pos] = {
            **position, f"{option}": value
        }

    def validate_invalid_stop(self, close, stop_price, position, spread, current_date):
        if (
            (position["type"] == self.BUY and stop_price > close)
            or
            (position["type"] == self.SELL and stop_price < (close + spread))
        ):
            raise Exception(f"""
                Invalid stop: {stop_price} at current price: {close},
                date_open: {position['date_open']},
                date_close: {position['date_close']},
                spread: {spread},
                current_date: {current_date},
                type_operation: {"BUY" if position['type'] == self.BUY else "SELL"},
            """)
