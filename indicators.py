import pandas_ta as ta

class Indicators:
    def __init__(self, config_value, indicators_params, data):
        self.config_value = config_value
        self.indicators_params = indicators_params
        self.data = data
        self._module = None

    def choose_algorithms(self):
        _copy = self.data.copy()
        for index, parameter in enumerate(self.indicators_params):
            params = {"length": self.config_value[index]}
            _copy[f"{parameter['function']}_{params['length']}_{index}"] = (
                self.select_algorithm(
                    _copy,
                    parameter["function"],
                    params,
                    index
                )
            )
        return _copy

    def select_algorithm(self, data, function, params, index):
        return getattr(data.ta, function)(**params)
