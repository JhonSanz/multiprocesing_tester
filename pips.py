class Pips:
    def __init__(self, decimals, volume, contract_size):
        self.decimals = decimals
        self.volume = volume
        self.contract_size = contract_size
    
    def unit_total(self):
        return self.volume * self.contract_size
    
    def pip_value(self):
        return 10 * self.unit_total() * 10**(-self.decimals)

    def convert_to_pips(self, value):
        return value / 10**(-self.decimals + 1)

    def profit(self, value):
        return self.pip_value() * self.convert_to_pips(value)
