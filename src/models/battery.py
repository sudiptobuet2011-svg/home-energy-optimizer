class Battery:
    SAVED_VALUES = {
        "capacity_kwh": 5.0,
        "max_charge_power_kw": 3.84,
        "max_discharge_power_kw": 3.84,
        "soc_initial_kwh": 0.0,
        "efficiency": 0.9,
    }

    def __init__(
        self,
        capacity_kwh,
        max_charge_power_kw,
        max_discharge_power_kw,
        soc_initial_kwh,
        efficiency,
    ):
        self.capacity_kwh = capacity_kwh
        self.max_charge_power_kw = max_charge_power_kw
        self.max_discharge_power_kw = max_discharge_power_kw
        self.soc_initial_kwh = soc_initial_kwh
        self.efficiency = efficiency

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
            value = input("Do you want to take saved battery values? (yes/no): ").strip().lower()
            if value in {"yes", "y"}:
                return True
            if value in {"no", "n"}:
                return False
            print("Please answer yes or no.")

    @classmethod
    def from_user_input(cls):
        print("\n--- Home Battery Configuration ---")

        if cls._use_saved_values():
            print("Using saved battery values:")
            print(f"capacity_kwh: {cls.SAVED_VALUES['capacity_kwh']} kWh")
            print(f"max_charge_power_kw: {cls.SAVED_VALUES['max_charge_power_kw']} kW")
            print(f"max_discharge_power_kw: {cls.SAVED_VALUES['max_discharge_power_kw']} kW")
            print(f"soc_initial_kwh: {cls.SAVED_VALUES['soc_initial_kwh']} kWh")
            print(f"efficiency: {cls.SAVED_VALUES['efficiency'] * 100}%")
            return cls(**cls.SAVED_VALUES)

        capacity_kwh = cls._get_positive_float("Battery capacity (kWh): ")
        max_charge_power_kw = cls._get_positive_float("Max charge power (kW): ")
        max_discharge_power_kw = cls._get_positive_float("Max discharge power (kW): ")

        while True:
            efficiency = cls._get_positive_float("Battery efficiency (0-1): ")
            if efficiency <= 1:
                break
            print("Efficiency must be less than or equal to 1.")

        while True:
            soc_initial_kwh = cls._get_non_negative_float("Initial battery level (kWh): ")
            if soc_initial_kwh <= capacity_kwh:
                break
            print("Initial SOC cannot exceed battery capacity.")

        return cls(
            capacity_kwh,
            max_charge_power_kw,
            max_discharge_power_kw,
            soc_initial_kwh,
            efficiency,
        )

    def __str__(self):
        return (
            "Battery("
            f"capacity_kwh={self.capacity_kwh}, "
            f"max_charge_power_kw={self.max_charge_power_kw}, "
            f"max_discharge_power_kw={self.max_discharge_power_kw}, "
            f"soc_initial_kwh={self.soc_initial_kwh}, "
            f"efficiency={self.efficiency}"
            ")"
        )
