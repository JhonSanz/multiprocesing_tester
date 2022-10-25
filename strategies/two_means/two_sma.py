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
        self.data.loc[:, "trend"] = None
        self.data.loc[self.data["close"] >= self.data[f"{high_label}"], ["trend"]] = self.UP_TREND
        self.data.loc[self.data["close"] <= self.data[f"{low_label}"], ["trend"]] = self.DOWN_TREND
        self.data.to_csv("test_data_indicators.csv", index=False)
        return
        for (
            date, close, sma_high, sma_low, trend
        ) in zip(
            self.data["date"], self.data["close"],
            self.data[r"SMA_[\d]+_0"],
            self.data[r"SMA_[\d]+_1"],
            self.data["trend"]
        ):
            if (close < sma_low and trend == self.UP_TREND):
                pass
