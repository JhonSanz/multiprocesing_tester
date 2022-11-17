class InvalidStopException(Exception):
    def __init__(self, stop, price):
        self.stop = stop
        self.price = price
        self.message = f"Invalid stop {self.stop} at {self.price}"
        super().__init__(self.message)
