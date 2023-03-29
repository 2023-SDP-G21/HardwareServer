import json


class MessageGeneration:
    DATA_CODE = 0
    WARNING_CODE = 1

    @staticmethod
    def generate_sensor_data(speed=None, battery=None):
        json_string = {"battery": battery, "speed": speed}
        return MessageGeneration.DATA_CODE, json.dumps(json_string)

    @staticmethod
    def generate_warning_data(warning_code):
        json_string = {"code": warning_code}
        return MessageGeneration.WARNING_CODE, json.dumps(json_string)
