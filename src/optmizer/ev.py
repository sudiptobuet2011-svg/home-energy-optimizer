from datetime import datetime


class EV:
    SAVED_VALUES = {
        "charging_start": "19:00",
        "charging_end": "07:00",
        "capacity_kwh": 100.0,
        "max_power_kw": 10.0,
        "soc_initial_kwh": 20.0,
        "soc_target_kwh": 100.0,
    }

    def __init__(
        self,
        charging_start,
        charging_end,
        capacity_kwh,
        max_power_kw,
        soc_initial_kwh,
        soc_target_kwh,
    ):
        self.charging_start = charging_start
        self.charging_end = charging_end
        self.capacity_kwh = capacity_kwh
        self.max_power_kw = max_power_kw
        self.soc_initial_kwh = soc_initial_kwh
        self.soc_target_kwh = soc_target_kwh

    @staticmethod
    def _get_time(prompt):
        while True:
            value = input(prompt)
            try:
                datetime.strptime(value, "%H:%M")
                return value
            except ValueError:
                print("Invalid format. Please use HH:MM (example: 18:00)")

    @staticmethod
    def _get_positive_float(prompt):
        while True:
            try:
                value = float(input(prompt))
                if value > 0:
                    return value
                print("Value must be positive.")
            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def _get_non_negative_float(prompt):
        while True:
            try:
                value = float(input(prompt))
                if value >= 0:
                    return value
                print("Value must be zero or positive.")
            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def _use_saved_values():
        while True:
            value = input("Do you want to take saved values? (yes/no): ").strip().lower()
            if value in {"yes", "y"}:
                return True
            if value in {"no", "n"}:
                return False
            print("Please answer yes or no.")

    @classmethod
    def from_user_input(cls):
        print("\n--- EV Charging Configuration ---")

        if cls._use_saved_values():
            print("Using saved EV values:")
            print(f"Charging start time (HH:MM): {cls.SAVED_VALUES['charging_start']}")
            print(f"Charging end time (HH:MM): {cls.SAVED_VALUES['charging_end']}")
            print(f"Battery capacity (kWh): {cls.SAVED_VALUES['capacity_kwh']}")
            print(f"Max charging power (kW): {cls.SAVED_VALUES['max_power_kw']}")
            print(f"Current battery level (kWh): {cls.SAVED_VALUES['soc_initial_kwh']}")
            print(f"Target battery level (kWh): {cls.SAVED_VALUES['soc_target_kwh']}")
            return cls(**cls.SAVED_VALUES)

        charging_start = cls._get_time("Charging start time (HH:MM): ")
        charging_end = cls._get_time("Charging end time (HH:MM): ")

        capacity_kwh = cls._get_positive_float("Battery capacity (kWh): ")
        max_power_kw = cls._get_positive_float("Max charging power (kW): ")

        while True:
            soc_initial_kwh = cls._get_non_negative_float("Current battery level (kWh): ")
            if soc_initial_kwh <= capacity_kwh:
                break
            print("Initial SOC cannot exceed battery capacity.")

        while True:
            soc_target_kwh = cls._get_positive_float("Target battery level (kWh): ")
            if soc_target_kwh <= capacity_kwh and soc_target_kwh >= soc_initial_kwh:
                break
            print("Target SOC must be >= initial SOC and <= battery capacity.")

        return cls(
            charging_start,
            charging_end,
            capacity_kwh,
            max_power_kw,
            soc_initial_kwh,
            soc_target_kwh,
        )

    def energy_needed(self):
        return max(self.soc_target_kwh - self.soc_initial_kwh, 0)

    def __str__(self):
        return (
            "EV("
            f"charging_start={self.charging_start}, "
            f"charging_end={self.charging_end}, "
            f"capacity_kwh={self.capacity_kwh}, "
            f"max_power_kw={self.max_power_kw}, "
            f"soc_initial_kwh={self.soc_initial_kwh}, "
            f"soc_target_kwh={self.soc_target_kwh}"
            ")"
        )
