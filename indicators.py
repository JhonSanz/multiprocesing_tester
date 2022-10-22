import importlib

class Indicators:
    def __init__(self, parameters, data):
        self.data = data
        self._parameters = parameters
        self._module = None
    
    @property
    def module(self):
        return self._module
    
    @module.setter
    def module(self, module):
        self._module = module

    def validate_strategy_file(self):
        try:
            return importlib.import_module(
                f"strategies.{self._strategy['file']}"
            )
        except ModuleNotFoundError:
            raise Exception(f"File {self._strategy['file']} not found")

    def run(self, data, indicators, ia_signal):
        return (
            getattr(self._module, 'Strategy')
            (self._strategy["params"])
            .get_signal(data, indicators, ia_signal)
        )

    def choose_algorithms(self):
        _copy = self.data.copy()
        for parameter in self._parameters:
            self.data = (
                self.select_algorithm(
                    _copy,
                    parameter["function"],
                    parameter["params"]
                )
            )
        return _copy

    def select_algorithm(self):
        getattr(self.data.ta, self.algorithm)(**self.params, append=True)
        return self.data
