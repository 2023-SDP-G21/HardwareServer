import unittest
from unittest.mock import patch, MagicMock
from queue import Queue
from collections import deque
from hardware_server.bluetooth import Bluetooth


class TestBluetooth(unittest.TestCase):
    def setUp(self):
        self.bluetooth = Bluetooth()

    def tearDown(self):
        pass

    def test_init(self):
        self.assertTrue(self.bluetooth._connected)
        self.assertIsInstance(self.bluetooth.send_queue, Queue)
        self.assertIsInstance(self.bluetooth.receive_queue, deque)

    def test_receive_data(self):
        # Test that receive_data() returns a copy of the receive queue
        self.bluetooth.receive_queue = deque([1, 2, 3])
        receive_copy = self.bluetooth.receive_data()
        self.assertListEqual(list(receive_copy), list(self.bluetooth.receive_queue))

    def test_send_data(self):
        # Test that send_data() adds data to the send queue
        self.bluetooth.send_data((1, 'hello'))
        self.assertEqual(self.bluetooth.send_queue.qsize(), 1)

    @patch('hardware_server.bluetooth.time.sleep', MagicMock())
    @patch('hardware_server.bluetooth.socket.socket', MagicMock())
    def test_initialise_connection(self):
        # Setup
        bt = Bluetooth()
        bt._sock.bind = MagicMock()
        bt._sock.listen = MagicMock()
        bt._sock.accept = MagicMock(return_value=(MagicMock(), ('test_address', 'test_port')))
        bt.initialise_connection()

        # Assertions
        bt._sock.bind.assert_called_once_with(('B8:27:EB:C4:80:A1', 1))
        bt._sock.listen.assert_called_once()
        bt._sock.accept.assert_called_once()
        self.assertTrue(bt._connected)
        self.assertIsNotNone(bt.send_queue)
        self.assertIsNotNone(bt.receive_queue)
        self.assertIsNotNone(bt.receive_lock)

        bt._sock.close()


if __name__ == '__main__':
    unittest.main()
