import io
import random
import struct
import sys
import unittest

from hardware_server.header import Header


class HeaderTest(unittest.TestCase):

    def test_valid_input(self):
        test_header = struct.pack("!??BB", False, False, 1, 10)
        header = Header.from_bytes(test_header)
        self.assertEqual(header.heartbeat_ack, False)
        self.assertEqual(header.heartbeat, False)
        self.assertEqual(header.data_type, 1)
        self.assertEqual(header.data_len, 10)

    def test_valid_input_100_times(self):
        for i in range(100):
            heartbeat_ack = random.choice([True, False])
            heartbeat = random.choice([True, False])
            data_type = random.randint(0, 255)
            data = random.randint(0, 255)
            test_header = struct.pack("!??BB", heartbeat_ack, heartbeat, data_type, data)
            header = Header.from_bytes(test_header)
            self.assertEqual(header.heartbeat_ack, heartbeat_ack)
            self.assertEqual(header.heartbeat, heartbeat)
            self.assertEqual(header.data_type, data_type)
            self.assertEqual(header.data_len, data)

    def test_invalid_format(self):
        test_header = struct.pack("!ii", 1, 10)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        Header.from_bytes(test_header)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "Could not unpack\n")

    def test_repr(self):
        test_header = struct.pack("!??BB", False, False, 1, 10)
        header = Header.from_bytes(test_header)
        self.assertEqual(str(header), "False False 1 10")


if __name__ == '__main__':
    unittest.main()
