US100_PARAMS = {
    "decimals": 1,
    "deposit": 10000,
    "volume": 0.1,
    "contract_size": 1,
    "swap_rates": {
        "monday": 1,
        "tuesday": 1,
        "wednesday": 1,
        "thursday": 1,
        "friday": 3,
    },
    "swap_long": -6.3,
    "swap_short": 1.3
}

EURUSD_PARAMS = {
    "decimals": 5,
    "deposit": 10000,
    "volume": 0.1,
    "contract_size": 100000,
    "swap_rates": {
        "monday": 1,
        "tuesday": 1,
        "wednesday": 3,
        "thursday": 1,
        "friday": 1,
    },
    "swap_long": -9.18,
    "swap_short": 5.34
}

CONFIGS = {
    "us100": {**US100_PARAMS},
    "eurusd": {**EURUSD_PARAMS}
}
