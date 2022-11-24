from pips import Pips

class Statistics:
    BUY = 0
    SELL = 1

    def __init__(self, data, indicators, pips_calculator):
        self.data = data
        self.indicators = indicators
        self.pips_calculator = pips_calculator

    def run(self):
        orders = self.data.copy()
        orders['total'] = orders['price_close'] - orders['price_open']
        orders.loc[orders['type'] == self.SELL, 'total'] = orders['total'] * (-1)
        orders["total"] = orders["total"].apply(lambda x: self.pips_calculator.profit(x))
        orders.to_csv(f"totals/{'_'.join(map(str, self.indicators))}_totals.csv")
        return orders
