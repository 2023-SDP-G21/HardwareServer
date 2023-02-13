import socket
import struct
from collections import deque
from queue import Queue
import threading
from MessageGeneration import MessageGeneration
import random
import time


class TCP:
    IP_ADDRESS = "172.20.101.231"
    PORT = 5000

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.IP_ADDRESS, self.PORT))
        self.send_queue = Queue()
        self.receive_queue = deque()
        self.receive_lock = threading.Lock()

    def _send_thread(self):
        while True:
            if self.send_queue:
                data = self.send_queue.get()
                # first char is converted to 1 byte so that app knows what kind of message that is (0 or 1)
                self.socket.sendall(data.encode("utf-8"))

    def _receive_thread(self):
        while True:
            data = self.socket.recv(8)
            if not data:
                continue
            speed, power = struct.unpack("!ii", data)
            with self.receive_lock:
                self.receive_queue.append((speed, power))
                print(speed, power)

    def receive_data(self):
        with self.receive_lock:
            return self.receive_queue.copy()

    def send_data(self, data):
        self.send_queue.put(data)

    def run(self):
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
