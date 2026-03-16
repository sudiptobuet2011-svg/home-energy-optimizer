import pandas as pd
from battery import Battery
from battery_charging import simulate_battery_operation
from ev import EV
from ev_charging import get_ev_charging_hours

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
df = df.sort_index()
df["pv_available_after_base"] = (df["pv_generation"] - df["base_load"]).clip(lower=0)

display_df = df[["pv_generation", "base_load", "pv_available_after_base"]].copy()
display_df.index = display_df.index.strftime("%H:%M")
print(display_df)



# ---- EV configuration ----
ev = EV.from_user_input()

print(ev)
print("Energy needed:", ev.energy_needed(), "kWh")

# ---- Home battery configuration ----
battery = Battery.from_user_input()

print(battery)

get_ev_charging_hours(df, ev)
fetched_from_pv, fetched_from_net, soc_real, battery_operation_df = simulate_battery_operation(df, battery)

print("\n--- Battery Charging Summary ---")
print(f"Total fetched from PV: {fetched_from_pv:.2f} kWh")
print(f"Total fetched from net: {fetched_from_net:.2f} kWh")
print(f"SOC real: {soc_real:.2f} kWh")

print("\n--- Battery Discharging Table ---")
display_battery_discharging_df = battery_operation_df[
    [
        "soc_real_after_discharge",
        "soc_real_after_charge",
        "charge_from_pv",
        "sold_energy",
        "price",
        "revenue",
    ]
].copy()
display_battery_discharging_df["soc_real_after_discharge"] = display_battery_discharging_df["soc_real_after_discharge"].map(lambda value: f"{value:.2f} kWh")
display_battery_discharging_df["soc_real_after_charge"] = display_battery_discharging_df["soc_real_after_charge"].map(lambda value: f"{value:.2f} kWh")
display_battery_discharging_df["charge_from_pv"] = display_battery_discharging_df["charge_from_pv"].map(lambda value: f"{value:.2f} kWh")
display_battery_discharging_df["sold_energy"] = display_battery_discharging_df["sold_energy"].map(lambda value: f"{value:.2f} kWh")
display_battery_discharging_df["price"] = display_battery_discharging_df["price"].map(lambda value: f"{value:.2f} EUR/MWh")
display_battery_discharging_df["revenue"] = display_battery_discharging_df["revenue"].map(lambda value: f"{value:.2f} EUR")
display_battery_discharging_df = display_battery_discharging_df.rename(
    columns={
        "soc_real_after_discharge": "SOC after discharge (kWh)",
        "soc_real_after_charge": "SOC after charge (kWh)",
        "charge_from_pv": "Charge from PV (kWh)",
        "sold_energy": "Sold energy (kWh)",
        "price": "Price (EUR/MWh)",
        "revenue": "Revenue (EUR)",
    }
)
display_battery_discharging_df.index = display_battery_discharging_df.index.strftime("%H:%M")
print(display_battery_discharging_df)
