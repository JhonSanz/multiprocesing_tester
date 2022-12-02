import re
from strategies.base_strategy import BaseStrategy
from datetime import datetime
from strategies.utils import InvalidStopException

class Strategy(BaseStrategy):
    UP_TREND = 1
    DOWN_TREND = -1
    RANGE = 0
    STOP = 700
    SPREAD = 10000000

    def __init__(self, data, decimals):
        super().__init__()
        self.data = data
        self.decimals = 10**(-decimals)
        self.high_label = ""
        self.low_label = ""
        self.SPREAD *= self.decimals
        self.STOP *= self.decimals
        self.higher_close = None

    def get_column_names(self, pattern):
        columns = self.data.columns
        p = re.compile(pattern)
        return list(filter(
            lambda y: y is not None,
            map(lambda x: p.search(x), columns)
        ))[0].group(0)

    def update_stop(self, pos_info, close, spread, sma_high, sma_low, date):
        if pos_info["direction"] != self._IN:
            return
        if close < sma_low:
            new_stop = close + spread + self.STOP
        elif close > sma_high:
            new_stop = close - self.STOP
        try:
            self.edit_position(close, spread, pos_info, "stop_loss", new_stop)
        except InvalidStopException as e:
            pass # print(e, date)

    def validate_higher_close(self, close, sma_high, sma_low):
        condition = (
            (close < sma_low and self.higher_close > close)
            or
            (close > sma_high and self.higher_close < close)
        )
        return condition

    def run(self):
        self.high_label = self.get_column_names("sma_[\d]+_0")
        self.low_label = self.get_column_names("sma_[\d]+_1")
        _data = self.data.copy()
        opened_position = False
        ticket = 0
        limit_low = None
        limit_high = None
        self.higher_close = self.data.iloc[0]["close"]
        new_close = False
        for (
            date, close, _open, high, low, sma_high, sma_low, spread
        ) in zip(
            _data["date"], _data["close"], _data["open"], _data["high"],  _data["low"],
            _data[f"{self.high_label}"], _data[f"{self.low_label}"], _data["spread"]
        ):
            spread = spread * self.decimals
            if (
                not (
                    date.time() >= datetime.strptime("01:50", "%H:%M").time()
                    and
                    date.time() <= datetime.strptime("22:59", "%H:%M").time()
                )
            ):
                continue

            self.validate_stop_losses(
                date, high, low, spread,
                close if date.time() == datetime.strptime("01:50", "%H:%M").time() else None,
            )
            if self.validate_higher_close(close, sma_high, sma_low):
                self.higher_close = close
                new_close = True
            if opened_position:
                pos_info = self.get_position_by_ticket(ticket)
                if new_close:
                    self.update_stop(pos_info, close, spread, sma_high, sma_low, date)
                if (
                    (
                        pos_info["type"] == self.SELL
                        and limit_low
                        and close > sma_low
                        and close > sma_high
                    )
                ):
                    self.close_operation(pos_info["date_open"], date, close)
                    opened_position = False
                if (
                    (
                        pos_info["type"] == self.BUY
                        and limit_high
                        and close < sma_low
                        and close < sma_high
                    )
                ):
                    self.close_operation(pos_info["date_open"], date, close)
                    opened_position = False
            if not opened_position:
                if (high < sma_low and limit_high and spread <= self.SPREAD):
                    ticket = self.open_operation(
                        close, date, self.SELL, spread,
                        close + self.STOP
                    )
                    opened_position = True
                    limit_high = False
                if (low > sma_high and limit_low and spread <= self.SPREAD):
                    ticket = self.open_operation(
                        close, date, self.BUY, spread,
                        close - self.STOP
                    )
                    opened_position = True
                    limit_low = False

            if (close < sma_low):
                limit_low = True
            elif (close > sma_high):
                limit_high = True
            new_close = False

        return self.save_orders(f"{self.high_label}_{self.low_label}")
