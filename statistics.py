from pips import Pips
from swap import Swap

class Statistics:
    BUY = 0
    SELL = 1

    def __init__(self, data, indicators, strategy_params):
        self.data = data
        self.indicators = indicators
        self.strategy_params = strategy_params

    def run(self):
        orders = self.data.copy()
        pips_calculator = Pips(
            self.strategy_params["params"]["decimals"],
            self.strategy_params["params"]["volume"],
            self.strategy_params["params"]["contract_size"],
        )
        swap_calculator = Swap(orders, self.strategy_params)
        orders = swap_calculator.run()
        orders['total'] = orders['price_close'] - orders['price_open'] + orders['swap']
        orders.loc[orders['type'] == self.SELL, 'total'] = orders['total'] * (-1)
        orders["total"] = orders["total"].apply(lambda x: pips_calculator.profit(x))
        orders.to_csv(f"totals/{'_'.join(map(str, self.indicators))}_totals.csv")
        return orders
