from datetime import datetime, timedelta

DAYS = {
    "saturday": 5,
    "sunday": 6
}

class Swap:
    BUY = 0
    SELL = 1
    def __init__(self, data, configs):
        self.data = data
        self.configs = configs

    def compute_days(self, row):
        return (row["date_close"].date() - row["date_open"].date()).days

    def formula(self, date, row):
        if date.weekday() in [DAYS["saturday"], DAYS["sunday"]]:
            return 0
        return (
            10 ** (-self.configs["params"]["decimals"]) * 10 * self.configs["params"]["volume"] *
            self.configs["params"]["contract_size"] * (
                self.configs["params"]["swap_long"] if row["type"] == self.BUY
                else self.configs["params"]["swap_short"]
            ) * self.configs["params"]["swap_rates"][date.strftime("%A").lower()]
        ) / 10

    def compute_swap(self, row):
        total = 0
        days = self.compute_days(row)
        for i in range(days):
            new_day = row["date_open"] + timedelta(days=i)
            total += self.formula(new_day, row)
        return total

    def run(self):
        data = self.data.copy()
        data["swap"] = data.apply(lambda x: self.compute_swap(x), axis=1)
        return data
