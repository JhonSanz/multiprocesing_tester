
class Statistics:
    BUY = 0
    SELL = 1

    def __init__(self, data, indicators):
        self.data = data
        self.indicators = indicators

    def run(self):
        orders = self.data.copy()
        orders['total'] = orders['price_close'] - orders['price_open']
        orders.loc[orders['type'] == self.SELL, 'total'] = orders['total'] * (-1)
        orders = orders[[
            'date_open', 'price_open', 'date_close',
            'price_close', 'type', 'total',
        ]]
        # orders.to_csv(f"totals/{'_'.join(map(str, self.indicators))}_totals.csv")
        return orders
