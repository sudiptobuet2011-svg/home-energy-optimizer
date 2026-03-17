from models.battery import Battery
from models.ev import EV
from models.pv_system import PVSystem
from optimizer.battery_dispatch import simulate_battery_operation
from optimizer.ev_optimizer import get_ev_charging_hours
from simulation.energy_balance import build_energy_balance, get_default_price_file


def main():
    df = build_energy_balance(get_default_price_file(), PVSystem())

    display_df = df[["pv_generation", "base_load", "pv_available_after_base"]].copy()
    display_df.index = display_df.index.strftime("%H:%M")
    print(display_df)

    ev = EV.from_user_input()
    print(ev)
    print("Energy needed:", ev.energy_needed(), "kWh")

    battery = Battery.from_user_input()
    print(battery)

    get_ev_charging_hours(df, ev)
    fetched_from_pv, fetched_from_net, soc_real, battery_operation_df = simulate_battery_operation(
        df,
        battery,
    )

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
    display_battery_discharging_df["soc_real_after_discharge"] = display_battery_discharging_df[
        "soc_real_after_discharge"
    ].map(lambda value: f"{value:.2f} kWh")
    display_battery_discharging_df["soc_real_after_charge"] = display_battery_discharging_df[
        "soc_real_after_charge"
    ].map(lambda value: f"{value:.2f} kWh")
    display_battery_discharging_df["charge_from_pv"] = display_battery_discharging_df[
        "charge_from_pv"
    ].map(lambda value: f"{value:.2f} kWh")
    display_battery_discharging_df["sold_energy"] = display_battery_discharging_df[
        "sold_energy"
    ].map(lambda value: f"{value:.2f} kWh")
    display_battery_discharging_df["price"] = display_battery_discharging_df["price"].map(
        lambda value: f"{value:.2f} EUR/MWh"
    )
    display_battery_discharging_df["revenue"] = display_battery_discharging_df["revenue"].map(
        lambda value: f"{value:.2f} EUR"
    )
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


if __name__ == "__main__":
    main()
