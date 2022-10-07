import numpy as np
import pandas as pd

class Strategy:
    def __init__(self, params = {}):
        self.params = params

    def get_signal(self, data, indicators, ia_signal):
        return "buy"
