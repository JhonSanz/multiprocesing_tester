import re
from strategies.base_strategy import BaseStrategy

class TwoMeansStrategy(BaseStrategy):
    UP_TREND = 1
    DOWN_TREND = -1
    RANGE = 0

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.high_label = ""
        self.low_label = ""

    def get_column_names(self, pattern):
        columns = self.data.columns
        p = re.compile(pattern)
        return list(filter(
            lambda y: y is not None,
            map(lambda x: p.search(x), columns)
        ))[0].group(0)

    def run(self):
        self.high_label = self.get_column_names("sma_[\d]+_0")
        self.low_label = self.get_column_names("sma_[\d]+_1")
        _data = self.data.copy()
        _data.loc[:, "trend"] = 0
        _data.loc[_data["close"] >= _data[f"{self.high_label}"], ["trend"]] = self.UP_TREND
        _data.loc[_data["close"] <= _data[f"{self.low_label}"], ["trend"]] = self.DOWN_TREND

        opened_position = False
        ticket = 0
        for (
            date, close, sma_high, sma_low, trend
        ) in zip(
            _data["date"], _data["close"], _data[f"{self.high_label}"],
            _data[f"{self.low_label}"], _data["trend"]
        ):
            if not opened_position:
                if (close < sma_low and trend == self.UP_TREND):
                    ticket = self.open_operation(close, date, self.SELL)
                    opened_position = True
                if (close > sma_high and trend == self.DOWN_TREND):
                    ticket = self.open_operation(close, date, self.SELL)
                    opened_position = True
            else:
                self.validate_stop_losses(date, close)
                pos_info = self.get_position_by_ticket(ticket)
                if (
                    (
                        pos_info["type"] == self.SELL
                        and trend == self.DOWN_TREND
                        and close > sma_low
                    ) or (
                        pos_info["type"] == self.BUY
                        and trend == self.UP_TREND
                        and close < sma_high
                    )
                ):
                    self.close_operation(pos_info["date_open"], date, close)
        self.save_orders(f"{self.high_label}_{self.low_label}")
