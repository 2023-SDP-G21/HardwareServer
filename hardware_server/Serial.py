import struct
import threading
from asyncio import Queue
from collections import deque

import serial

from hardware_server import Packet
from hardware_server.Header import Header


class Serial:
    """
    Serial communication class
    """
    serial_port = "COM3"
    baud_rate = 9600

    def __init__(self):
        """
        Initialize serial connection
        """
        self.conn = serial.Serial(self.serial_port, self.baud_rate, timeout=0.1)
        self.send_queue = Queue()
        self.receive_queue = deque()
        self.receive_lock = threading.Lock()

    def _send_thread(self):
        """
        Creates thread to send data to the serial port
        :return: None
        """
        while True:
            if self.send_queue:
                data_type, data = self.send_queue.get()
                packet_bytes = Packet.as_bytes(False, False, data_type, data)
                self.conn.write(packet_bytes)

    def _receive_thread(self):
        """
        Creates thread to receive data from the serial port
        :return: None
        """
        while True:
            packet_bytes = self.conn.read(Header.HEADER_LEN)
            if not packet_bytes:
                continue

            header = Header.from_bytes(packet_bytes)
            data_bytes = self.conn.read(header.data_len)
            data = struct.unpack("!ii", data_bytes)
            with self.receive_lock:
                self.receive_queue.append(data)

    def receive_data(self):
        """
        Returns a copy of the receive queue
        :return: deque
        """
        with self.receive_lock:
            return self.receive_queue.copy()

    def send_data(self, data):
        """
        Adds data to the send queue
        :param data:
        :return: None
        """
        self.send_queue.put(data)

    def run(self):
        """
        Starts send and receive threads
        :return:
        """
        send_thread = threading.Thread(target=self._send_thread)
        receive_thread = threading.Thread(target=self._receive_thread)
        send_thread.start()
        receive_thread.start()
        self.conn.close()


if __name__ == '__main__':
    serial = Serial()
    serial.run()
