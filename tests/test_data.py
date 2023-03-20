import io
import random
import struct
import sys
import unittest

from hardware_server.data import Data


class DataTest(unittest.TestCase):
    def test_invalid_byte_format(self):
        test_string = "Hello world"
        test_string_bytes = test_string.encode()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Data.from_bytes(test_string_bytes)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "Could not unpack\n")

    def test_invalid_byte_length(self):
        test_ints = struct.pack("!iii", 1, 2, 3)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Data.from_bytes(test_ints)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "Could not unpack\n")

    def test_valid_decode(self):
        # write byte string for angle = 50 and power = 90
        test_angle_power = struct.pack("!ii", 50, 90)
        test_data = Data.from_bytes(test_angle_power)
        self.assertEqual(test_data.angle, 50)
        self.assertEqual(test_data.power, 90)

    def test_valid_assignment(self):
        test_angle_power = struct.pack("!ii", 0, 100)
        test_data = Data.from_bytes(test_angle_power)
        self.assertEqual(test_data.angle, 0)
        self.assertEqual(test_data.power, 100)

    def test_invalid_angle_range_lower_bound(self):
        test_angle_invalid = struct.pack("!ii", -181, 100)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Data.from_bytes(test_angle_invalid)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "Could not unpack\n")

    def test_invalid_angle_range_upper_bound(self):
        test_angle_invalid = struct.pack("!ii", 181, 100)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Data.from_bytes(test_angle_invalid)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "Could not unpack\n")

    def test_accepts_extreme_angles_neg_180(self):
        test_angle_power = struct.pack("!ii", -180, 100)
        test_data = Data.from_bytes(test_angle_power)
        self.assertEqual(test_data.angle, -180)
        self.assertEqual(test_data.power, 100)

    def test_accepts_extreme_angles_180(self):
        test_angle_power = struct.pack("!ii", 180, 100)
        test_data = Data.from_bytes(test_angle_power)
        self.assertEqual(test_data.angle, 180)
        self.assertEqual(test_data.power, 100)

    def test_accepts_normal_angles(self):
        rand_angle = random.randint(-180, 180)
        test_angle_power = struct.pack("!ii", rand_angle, 50)
        test_data = Data.from_bytes(test_angle_power)
        self.assertEqual(test_data.angle, rand_angle)

    def test_accepts_0_power(self):
        test_angle_power = struct.pack("!ii", 0, 0)
        test_data = Data.from_bytes(test_angle_power)
        self.assertEqual(test_data.angle, 0)
        self.assertEqual(test_data.power, 0)

    def test_accepts_100_power(self):
        test_angle_power = struct.pack("!ii", 0, 100)
        test_data = Data.from_bytes(test_angle_power)
        self.assertEqual(test_data.angle, 0)
        self.assertEqual(test_data.power, 100)

    def test_accepts_normal_power(self):
        rand_power = random.randint(0, 100)
        test_angle_power = struct.pack("!ii", 0, rand_power)
        test_data = Data.from_bytes(test_angle_power)
        self.assertEqual(test_data.power, rand_power)

    def test_rejects_negative_power(self):
        test_angle_power = struct.pack("!ii", 0, -1)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Data.from_bytes(test_angle_power)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "Could not unpack\n")

    def test_rejects_over_100_power(self):
        test_angle_power = struct.pack("!ii", 0, 101)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Data.from_bytes(test_angle_power)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "Could not unpack\n")

    def test_correct_str_repr(self):
        test_angle_power = struct.pack("!ii", 50, 90)
        test_data = Data.from_bytes(test_angle_power)
        self.assertEqual(str(test_data), "Angle: 50, Power: 90")


if __name__ == '__main__':
    unittest.main()
