import math


def get_ev_charging_hours(df, ev):
    start_time = ev.charging_start
    end_time = ev.charging_end

    time_strings = df.index.strftime("%H:%M")
    if start_time <= end_time:
        filtered_df = df[(time_strings >= start_time) & (time_strings <= end_time)]
    else:
        filtered_df = df[(time_strings >= start_time) | (time_strings <= end_time)]

    ranked_hours = filtered_df.sort_values("price")
    available_hours = ranked_hours.index.tolist()

    charging_hours_needed = math.ceil(ev.energy_needed() / ev.max_power_kw)
    selected_hours = available_hours[:charging_hours_needed]
    selected_prices = ranked_hours["price"].tolist()[:charging_hours_needed]
    cost = [(price / 1000) * ev.max_power_kw for price in selected_prices]

    print("\n--- EV Charging Hours ---")
    print(f"{'Selected charging hour':<24} {'Cost':>8}")
    print(f"{'-' * 24} {'-' * 8}")
    for hour, value in zip(selected_hours, cost):
        print(f"{str(hour):<24} {value:>8.2f}")

    return selected_hours, cost
