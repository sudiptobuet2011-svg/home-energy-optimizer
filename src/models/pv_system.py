class PVSystem:
    DEFAULT_GENERATION_PROFILE = {
        "00:00": 0.0,
        "01:00": 0.0,
        "02:00": 0.0,
        "03:00": 0.0,
        "04:00": 0.0,
        "05:00": 0.0,
        "06:00": 0.0,
        "07:00": 0.0,
        "08:00": 0.15,
        "09:00": 0.65,
        "10:00": 1.4,
        "11:00": 2.2,
        "12:00": 2.6,
        "13:00": 2.2,
        "14:00": 1.3,
        "15:00": 0.6,
        "16:00": 0.2,
        "17:00": 0.0,
        "18:00": 0.0,
        "19:00": 0.0,
        "20:00": 0.0,
        "21:00": 0.0,
        "22:00": 0.0,
        "23:00": 0.0,
    }

    def __init__(self, generation_profile=None):
        self.generation_profile = generation_profile or self.DEFAULT_GENERATION_PROFILE.copy()

    def generation_for_timestamp(self, timestamp):
        return self.generation_profile.get(timestamp.strftime("%H:%M"), 0.0)
