import importlib

class Strategy:
    def __init__(self, strategy: dict):
        self._strategy = strategy
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
