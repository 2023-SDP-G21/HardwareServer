import json


class MessageGeneration:
    DATA_CODE = 0
    WARNING_CODE = 1

    def __init__(self):
        self.battery = 100
        self.speed = 0.0

    def generate_sensor_data(self, speed=None, battery=None):
        json_string = {}
        if speed or speed != self.speed:
            json_string["speed"] = self.speed = speed
        if battery or battery != self.battery:
            json_string["battery"] = self.battery = battery

        return str(self.DATA_CODE) + json.dumps(json_string)

    def generate_warning_data(self, code):
        json_string = {"code": code}
        return str(self.WARNING_CODE) + json.dumps(json_string)
