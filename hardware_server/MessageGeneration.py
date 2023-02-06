import json

class MessageGeneration:

    @staticmethod
    def generate_sensor_data(battery, speed, time_since_start):
        data_dict = {
            "battery": battery,
            "speed": speed,
            "timeSinceStart": time_since_start
        }

        return json.dumps(data_dict)

    @staticmethod
    def generate_warning_message(message):
        warning_dict = {
            "type": message
        }

        return json.dumps(warning_dict)
