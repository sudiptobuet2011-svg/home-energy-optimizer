import pandas as pd


def discharge_battery_for_hour(soc_real, battery, price):
    max_sell_per_hour = battery.max_discharge_power_kw * battery.efficiency
    sold_energy = min(soc_real, max_sell_per_hour)
    revenue = sold_energy * price / 1000
    soc_after_discharge = soc_real - sold_energy

    return sold_energy, revenue, soc_after_discharge


def simulate_battery_operation(df, battery):
    soc_real = battery.soc_initial_kwh
    fetched_from_pv_total = 0.0
    hourly_rows = []

    for time, row in df.iterrows():
        soc_start = soc_real
        sold_energy, revenue, soc_after_discharge = discharge_battery_for_hour(
            soc_real,
            battery,
            row["price"],
        )

        remaining_capacity = battery.capacity_kwh - soc_after_discharge
        charge_from_pv = min(
            row["pv_available_after_base"],
            remaining_capacity,
            battery.max_charge_power_kw,
        )
        soc_real = soc_after_discharge + charge_from_pv
        fetched_from_pv_total += charge_from_pv

        hourly_rows.append(
            {
                "time": time,
                "soc_real_before_discharge": soc_start,
                "soc_real_after_discharge": soc_after_discharge,
                "price": row["price"],
                "sold_energy": sold_energy,
                "revenue": revenue,
                "charge_from_pv": charge_from_pv,
                "soc_real_after_charge": soc_real,
            }
        )

    fetched_from_net_total = max(battery.capacity_kwh - soc_real, 0)
    battery_operation_df = pd.DataFrame(hourly_rows).set_index("time")

    return fetched_from_pv_total, fetched_from_net_total, soc_real, battery_operation_df
