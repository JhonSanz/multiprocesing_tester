def cut_data(data, strategy_paramas, current_strategy_values):
    start_date = strategy_paramas['start_date']
    rest_rows = len(data[data["date"] < start_date])
    if any(map(lambda x: x >= rest_rows, current_strategy_values)):
        raise Exception("Not enought data")

    return data[data["date"] >= start_date]
