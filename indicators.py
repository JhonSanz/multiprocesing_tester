import pandas_ta as ta

class Indicators:
    def __init__(self, config_value, indicators_params, data):
        self.config_value = config_value
        self.indicators_params = indicators_params
        self.data = data
        self._module = None

    def choose_algorithms(self):
        _copy = self.data.copy()
        for parameter in self.indicators_params:
            self.data = (
                self.select_algorithm(
                    _copy,
                    parameter["function"],
                    {"length": self.config_value}
                )
            )
        return _copy

    def select_algorithm(self, data, function, params):
        getattr(data.ta, function)(**params, append=True)
        return self.data
