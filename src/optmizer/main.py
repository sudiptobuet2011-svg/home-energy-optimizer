import pandas as pd

prices = pd.read_csv("data/raw/day_ahead_prices.csv", sep=";", decimal=",")
pv = pd.read_csv("data/raw/pv_generation.csv", sep=";", decimal=",")
load = pd.read_csv("data/raw/consumption_profile.csv", sep=";", decimal=",")

prices = prices.rename(columns={"HourUTC": "time", "SpotPriceEUR": "price"})
pv = pv.rename(columns={"Zeit": "time", "PV": "pv_generation"})
load = load.rename(columns={"Zeit": "time", "Verbrauch": "base_load"})

prices["time"] = pd.to_datetime(prices["time"])
pv["time"] = pd.to_datetime(pv["time"])
load["time"] = pd.to_datetime(load["time"])

df = prices.merge(pv, on="time").merge(load, on="time")

df = df.set_index("time")

print(df.head())