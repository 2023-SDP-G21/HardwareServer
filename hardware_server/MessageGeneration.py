import json
import struct


class MessageGeneration:
    DATA_CODE = 0
    WARNING_CODE = 1
    battery = 100
    speed = 0.0

    @staticmethod
    def generate_sensor_data(speed=None, battery=None):
        json_string = {}
        if battery or battery != battery:
            json_string["battery"] = MessageGeneration.battery = battery
        if speed or speed != speed:
            json_string["speed"] = MessageGeneration.speed = speed
        return str(MessageGeneration.DATA_CODE) + json.dumps(json_string)

    @staticmethod
    def generate_warning_data(warning_code):
        json_string = {"code": warning_code}
        return str(MessageGeneration.WARNING_CODE) + json.dumps(json_string)
