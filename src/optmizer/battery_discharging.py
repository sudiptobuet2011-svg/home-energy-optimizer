def discharge_battery_for_hour(soc_real, battery, price):
    max_sell_per_hour = battery.max_discharge_power_kw * battery.efficiency
    sold_energy = min(soc_real, max_sell_per_hour)
    revenue = sold_energy * price / 1000
    soc_after_discharge = soc_real - sold_energy

    return sold_energy, revenue, soc_after_discharge
