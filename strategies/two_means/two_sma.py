from strategies.base_strategy import BaseStrategy


class TwoMeansStrategy(BaseStrategy):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        for (
            date, close, sma11, sma_high, sma_close
        ) in zip(
            self.data["date"], self.data["close"],
            self.data[r"SMA_[\d]+_0"],
            self.data[r"SMA_[\d]+_1"],
        ):
            pass
