import pandas as pd

prices = pd.read_csv(
    "data/raw/day_ahead_prices.csv",
    sep=";",
    decimal=","
)

prices = prices.rename(columns={
    "HourUTC": "time",
    "SpotPriceEUR": "price"
})

print(prices.head())