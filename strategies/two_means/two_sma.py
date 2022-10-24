from strategies.base_strategy import BaseStrategy


class TwoMeansStrategy(BaseStrategy):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        for (
            date, close, sma11, sma265,
            chance_low, chance_high,
            cross_sma_low, cross_sma_high
        ) in zip(
            self.data["date"], self.data["close"], self.data[r"SMA_[\d]+_0"],
            self.data[r"SMA_[\d]+_1"],
        ):
            pass
