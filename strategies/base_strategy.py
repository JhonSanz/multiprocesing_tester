import pandas as pd

class BaseStrategy:
    BUY = 0
    SELL = 1

    def __init__(self):
        self.orders = []
    
    def open_operation(self, price, date, type):
        self.orders.append({"price": price, "date": date, "type": type})
    
    def save_orders(self):
        df = pd.DataFrame(data=self.orders)
        df.to_csv("orders.csv")
