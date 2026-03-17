from pathlib import Path

import pandas as pd


DEFAULT_BASE_LOAD_PROFILE = {
    "00:00": 0.2,
    "01:00": 0.18,
    "02:00": 0.18,
    "03:00": 0.18,
    "04:00": 0.22,
    "05:00": 0.35,
    "06:00": 0.75,
    "07:00": 0.95,
    "08:00": 0.6,
    "09:00": 0.45,
    "10:00": 0.4,
    "11:00": 0.55,
    "12:00": 0.85,
    "13:00": 0.55,
    "14:00": 0.45,
    "15:00": 0.5,
    "16:00": 0.75,
    "17:00": 1.1,
    "18:00": 1.4,
    "19:00": 1.3,
    "20:00": 1.1,
    "21:00": 0.7,
    "22:00": 0.45,
    "23:00": 0.25,
}


def build_energy_balance(price_file_path, pv_system):
    prices = pd.read_csv(price_file_path, sep=";", decimal=",")
    prices = prices.rename(columns={"HourUTC": "time", "SpotPriceEUR": "price"})
    prices["time"] = pd.to_datetime(prices["time"], dayfirst=True)
    prices = prices.sort_values("time").set_index("time")

    balance_df = prices.copy()
    balance_df["pv_generation"] = [
        pv_system.generation_for_timestamp(timestamp) for timestamp in balance_df.index
    ]
    balance_df["base_load"] = [
        DEFAULT_BASE_LOAD_PROFILE.get(timestamp.strftime("%H:%M"), 0.0)
        for timestamp in balance_df.index
    ]
    balance_df["pv_available_after_base"] = (
        balance_df["pv_generation"] - balance_df["base_load"]
    ).clip(lower=0)

    return balance_df


def get_default_price_file():
    return Path(__file__).resolve().parents[2] / "data" / "sample_day_ahead_prices.csv"
