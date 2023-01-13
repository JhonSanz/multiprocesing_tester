import re
from strategies.base_strategy import BaseStrategy
from datetime import datetime
from strategies.utils import InvalidStopException


class Strategy(BaseStrategy):
    UP_TREND = 1
    DOWN_TREND = -1
    RANGE = 0
    STOP = 1700
    SPREAD = 10000000
    ATR_MULTIPLIER = 10

    def __init__(self, data, decimals):
        super().__init__()
        self.data = data
        self.num_decimals = decimals
        self.decimals = 10**(-decimals)
        self.high_label = ""
        self.low_label = ""
        self.atr_label = ""
        self.SPREAD *= self.decimals
        self.STOP *= self.decimals
        self.higher_close = None

    def get_column_names(self, pattern):
        columns = self.data.columns
        p = re.compile(pattern)
        return list(filter(
            lambda y: y is not None,
            map(lambda x: p.search(x), columns)
        ))[0].group(0)

    def get_atr_stop_loss(self, current_atr, close, is_buy):
        new_stop_loss = 0
        if is_buy:
            new_stop_loss = close - (self.ATR_MULTIPLIER * current_atr)
        else:
            new_stop_loss = close + (self.ATR_MULTIPLIER * current_atr)

        # new_stop_loss = round(new_stop_loss, self.num_decimals)
        return new_stop_loss

    def update_atr_stop_loss(self, current_atr, close, is_buy, is_green):
        new_stop_loss = -1
        if (is_buy and is_green):
            new_stop_loss = self.get_atr_stop_loss(current_atr, close, True)
        elif (not is_buy and not is_green):
            new_stop_loss = self.get_atr_stop_loss(current_atr, close, False)
        return new_stop_loss

    def run(self):
        self.high_label = self.get_column_names("sma_[\d]+_0")
        self.low_label = self.get_column_names("sma_[\d]+_1")
        self.atr_label = self.get_column_names("atr_[\d]+_2")
        _data = self.data.copy()
        ticket = 0
        limit_low = None
        limit_high = None
        self.higher_close = self.data.iloc[0]["close"]
        for (
            date, close, _open,
            high, low,
            sma_high, sma_low,
            atr,
            spread
        ) in zip(
            _data["date"], _data["close"], _data["open"],
            _data["high"],  _data["low"],
            _data[f"{self.high_label}"], _data[f"{self.low_label}"],
            _data[f"{self.atr_label}"],
            _data["spread"]
        ):
            spread = spread * self.decimals
            if (
                not (
                    date.time() >= datetime.strptime("01:50", "%H:%M").time()
                    and
                    date.time() <= datetime.strptime("22:59", "%H:%M").time()
                )
            ):
                continue

            self.validate_stop_losses(
                date, high, low, spread,
                close if date.time() == datetime.strptime("01:50", "%H:%M").time() else None,
            )
            if self.opened_position:
                pos_info = self.get_position_by_ticket(ticket)
                # Actualiza el stop loss en cada tick
                new_stop = self.update_atr_stop_loss(
                    atr, close, pos_info["type"] == self.BUY,
                    (close > _open)
                )
                if (new_stop != -1):
                    self.edit_position(close, spread, pos_info, "stop_loss", new_stop, date)

                # Cierra la operacion cuando cruza otra vez las medias en la tendencia contraria
                if (
                    (
                        pos_info["type"] == self.SELL
                        and limit_low
                        and close > sma_low
                        and close > sma_high
                    )
                ):
                    self.close_operation(pos_info["date_open"], date, close)
                    self.opened_position = False
                if (
                    (
                        pos_info["type"] == self.BUY
                        and limit_high
                        and close < sma_low
                        and close < sma_high
                    )
                ):
                    self.close_operation(pos_info["date_open"], date, close)
                    self.opened_position = False
            if not self.opened_position:
                if (high < sma_low and limit_high and spread <= self.SPREAD):
                    position_stop = self.get_atr_stop_loss(atr, close, False)
                    ticket = self.open_operation(
                        close, date, self.SELL, spread,
                        position_stop
                    )
                    self.opened_position = True
                    limit_high = False

                if (low > sma_high and limit_low and spread <= self.SPREAD):
                    position_stop = self.get_atr_stop_loss(atr, close, True)
                    ticket = self.open_operation(
                        close, date, self.BUY, spread,
                        position_stop
                    )
                    self.opened_position = True
                    limit_low = False

            if (close < sma_low):
                limit_low = True
            elif (close > sma_high):
                limit_high = True

        return self.save_orders(f"{self.high_label}_{self.low_label}_{self.atr_label}")
