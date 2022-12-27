from DAL.SQL.sql import get_battery_id, get_battery_capacity, get_battery_consumption


class Battery:
    def __init__(self, user_id):
        self.user_id = user_id
        self.battery_id = get_battery_id(user_id)
        self.capacity = get_battery_capacity(self.battery_id)
        self.consumption = get_battery_consumption(self.battery_id)
