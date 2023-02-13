import json
import struct


class MessageGeneration:

    @staticmethod
    def generate_sensor_data(speed,battery):
        json_string = {}
        if battery != battery:
            json_string["battery"] = battery
            battery = battery
        elif speed != speed:
            json_string["speed"] = speed
            speed = speed

        return json.dumps(json_string)

    @staticmethod
    def generate_warning_data(warning_code):
        json_string = {}
        if warning_code != warning_code:
            json_string["warning_code"] = warning_code
            warning_code = warning_code

        return json.dumps(json_string)
