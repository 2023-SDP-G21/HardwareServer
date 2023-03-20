import random
import unittest

import hardware_server.packet as packet


class PacketTest(unittest.TestCase):
    def test_invalid_byte_format(self):
        test_string = "This should fail the tests"
        packet_bytes = packet.as_bytes(False, False, 1, test_string)
        self.assertEqual(None, packet_bytes)


if __name__ == '__main__':
    unittest.main()
