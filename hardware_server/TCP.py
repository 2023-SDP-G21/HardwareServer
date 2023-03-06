"""

"""

import socket
import struct
import threading
from collections import deque
from queue import Queue

from hardware_server import Packet
from Header import Header


class TCP:
    # IP_ADDRESS = "172.20.101.231"
    IP_ADDRESS = "localhost"
    PORT = 5000

    def __init__(self):
        """
        Initializes the TCP server.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # prevents OSError Address already in use exception
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.IP_ADDRESS, self.PORT))
        self.send_queue = Queue()
        self.receive_queue = deque()
        self.receive_lock = threading.Lock()

    def _send_thread(self):
        """
        Sends data from the send queue to the client.
        :return:
        """
        while True:
            if self.send_queue:
                data_type, data = self.send_queue.get()
                packet_bytes = Packet.as_bytes(False, False, data_type, data)
                self.socket.sendall(packet_bytes)

    def _receive_thread(self):
        """
        Receives data from the client and adds it to receive queue.
        :return:
        """
        while True:
            header_bytes = self.socket.recv(Header.HEADER_LEN)
            if not header_bytes:
                continue

            header = Header.from_bytes(header_bytes)
            data_bytes = self.socket.recv(header.data_len)
            data = struct.unpack("!ii", data_bytes)

            with self.receive_lock:
                self.receive_queue.append(data)

    def receive_data(self):
        """
        Returns a copy of receive queue.
        :return: copy of receive queue
        """
        with self.receive_lock:
            return self.receive_queue.copy()

    def send_data(self, data):
        """
        Adds data to send queue.
        :param data:
        :return:
        """
        self.send_queue.put(data)

    def run(self):
        """
        Starts the server.
        :return:
        """
        self.socket.listen(1)
        print("Waiting for a connection...")

        connection, client_address = self.socket.accept()
        self.socket = connection
        print("Connection from", client_address)

        send_thread = threading.Thread(target=self._send_thread)
        receive_thread = threading.Thread(target=self._receive_thread)

        send_thread.start()
        receive_thread.start()


if __name__ == "__main__":
    server = TCP()
    server.run()
