import unittest

from hardware_server.message_generation import MessageGeneration


class TestMessageGeneration(unittest.TestCase):

    def test_sensors_no_parameters(self):
        # Test case with no parameters
        expected = (MessageGeneration.DATA_CODE, '{}')
        self.assertEqual(expected, MessageGeneration.generate_sensor_data())

    def test_sensors_battery_parameter(self):
        # Test case with only battery parameter
        expected = (MessageGeneration.DATA_CODE, '{"battery": 50}')
        self.assertEqual(MessageGeneration.generate_sensor_data(battery=50), expected)

    def test_sensors_speed_parameter(self):
        # Test case with only speed parameter
        expected = (MessageGeneration.DATA_CODE, '{"speed": 30.0}')
        self.assertEqual(MessageGeneration.generate_sensor_data(speed=30.0), expected)

    def test_sensors_battery_speed_parameters(self):
        # Test case with both parameters
        expected = (MessageGeneration.DATA_CODE, '{"battery": 75, "speed": 20.0}')
        self.assertEqual(MessageGeneration.generate_sensor_data(speed=20.0, battery=75), expected)

    def test_generate_warning_data_valid_code(self):
        # Test case with valid warning code
        expected = (MessageGeneration.WARNING_CODE, '{"code": 1}')
        self.assertEqual(MessageGeneration.generate_warning_data(1), expected)

    def test_warning_data_invalid_code(self):
        # Test case with invalid warning code
        expected = (MessageGeneration.WARNING_CODE, '{"code": "invalid"}')
        self.assertEqual(MessageGeneration.generate_warning_data("invalid"), expected)
