import importlib


class StrategySelector:
    def __init__(self, strategy, data, params):
        self.strategy = strategy
        self.module = None
        self.data = data
        self.params = params

    def validate_strategy_file(self):
        try:
            self.module = importlib.import_module(
                f"strategies.{self.strategy}")
        except ModuleNotFoundError:
            raise Exception(f"File strategies.{self.strategy} not found")
        try:
            getattr(self.module, "Strategy")
        except AttributeError:
            raise Exception(
                f"File strategies.{self.strategy} has not Strategy class")

    def run_strategy(self):
        self.validate_strategy_file()
        strategy_class = getattr(self.module, "Strategy")
        return strategy_class(self.data, self.params).run()
