import importlib
import pandas_ta as ta

class AlgorithmSelector:
    def __init__(self, data, algorithm, params):
        self.data = data
        self.algorithm = algorithm
        self.params = params
        self.function = None
        self.module = None

    def validate_algorithm_params(self):
        if (
            set(self.params.keys()) !=
            set(self.function.__code__.co_varnames[1:])
        ):
            raise Exception(f"Invalid params {self.params} for {self.algorithm} function")

    def validate_algorithm_name(self):
        try:
            self.module = importlib.import_module(f"algorithms_repo.{self.algorithm}")
        except ModuleNotFoundError:
            raise Exception(f"File algorithms_repo.{self.algorithm} not found")
        try:
            self.function = getattr(self.module, self.algorithm)
        except AttributeError:
            raise Exception(f"Function {self.algorithm} not found")

    def select_algorithm(self):
        # self.validate_algorithm_name()
        # self.validate_algorithm_params()
        result = getattr(self.data.ta, self.algorithm)(**self.params)
        return result
