import re
from strategies.base_strategy import BaseStrategy

class TwoMeansStrategy(BaseStrategy):
    UP_TREND = 1
    DOWN_TREND = -1
    RANGE = 0

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.high = "sma_[\d]+_0"
        self.low = "sma_[\d]+_1"

    def get_column_names(self, pattern):
        columns = self.data.columns
        p = re.compile(pattern)
        return list(filter(lambda y: y is not None, map(lambda x: p.search(x), columns)))[0].group(0)

    def run(self):
        high_label = self.get_column_names(self.high)
        low_label = self.get_column_names(self.low)
        _data = self.data.copy()
        _data.loc[:, "trend"] = 0
        _data.loc[_data["close"] >= _data[f"{high_label}"], ["trend"]] = self.UP_TREND
        _data.loc[_data["close"] <= _data[f"{low_label}"], ["trend"]] = self.DOWN_TREND
        for (
            date, close, sma_high, sma_low, trend
        ) in zip(
            _data["date"], _data["close"], _data[f"{high_label}"],
            _data[f"{low_label}"], _data["trend"]
        ):
            if (close < sma_low and trend == self.UP_TREND):
                self.open_operation(close, date, self.SELL)
            if (close > sma_high and trend == self.DOWN_TREND):
                self.open_operation(close, date, self.SELL)

