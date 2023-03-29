import errno
import socket
import threading
import time
from collections import deque
from queue import Queue
from socket import error

from .packet import *
from .data import *
from .header import *


class Bluetooth:
    """
    Establishes a bluetooth connection and sends data
    """

    MAC_ADDRESS = "DC:A6:32:18:06:59"
    PORT = 5
    RESTART_TIME = 5

    def __init__(self):
        self._connected = True
        self.send_queue = Queue()
        self.receive_queue = deque()
        self.receive_lock = threading.Lock()
        self._sock = socket.socket(
            socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    def _send_thread(self, socket):
        """
        Sends data from the send queue to the client.
        :return:
        """
        while self._connected:
            if not self.send_queue.empty():
                data_type, data = self.send_queue.get()
                packet_bytes = as_bytes(False, False, data_type, data)
                try:
                    socket.send(packet_bytes)
                except error as e:
                    # if error HAS NOT occurred due to socket being set to nonblocking
                    if e.args[0] != errno.EWOULDBLOCK:
                        self._connected = False
                        break

    def _receive_thread(self, socket):
        """
        Receives data from the client and adds it to receive queue.
        :return:
        """
        while self._connected:
            try:
                header_bytes = socket.recv(Header.HEADER_LEN)
                if not header_bytes:
                    continue

                header = Header.from_bytes(header_bytes)
                data_bytes = socket.recv(header.data_len)
                data = Data.from_bytes(data_bytes)

                if not data:
                    continue

                with self.receive_lock:
                    self.receive_queue.append((data.angle, data.power))
            except error as e:
                # if error HAS NOT occurred due to socket being set to nonblocking
                if e.args[0] != errno.EWOULDBLOCK:
                    self._connected = False
                    break

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

    def initialise_connection(self):
        """
        Initialises new Bluetooth socket and accepts connection
        :return:
        """
        self._sock = socket.socket(
            socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.MAC_ADDRESS, self.PORT))
        self._sock.listen(1)

        print("Waiting for connection on RFCOMM channel", self.PORT)
        client_sock, client_info = self._sock.accept()
        client_sock.setblocking(False)
        print("Connection accepted from MAC", client_info[0])
        self._connected = True
        self.receive_queue = deque()
        self.receive_lock = threading.Lock()
        return client_sock
    
    def _run_thread(self):
        """
        Attempts sending/receiving data through the thread. Attempts reconnection upon error
        :return:
        """
        while True:
            print("Initializing connection...")

            client_sock = self.initialise_connection()

            # Attempt sending/receiving
            send_thread = threading.Thread(
                target=self._send_thread, args=(client_sock,))
            receive_thread = threading.Thread(
                target=self._receive_thread, args=(client_sock,))

            # Start threads
            send_thread.start()
            receive_thread.start()

            send_thread.join()
            receive_thread.join()

            client_sock.close()
            self._sock.close()

            print(f"Restarting connection in {self.RESTART_TIME} seconds...\n")
            time.sleep(self.RESTART_TIME)

    def run(self):
        run_thread = threading.Thread(target=self._run_thread, args=())
        run_thread.start()


if __name__ == "__main__":
    server = Bluetooth()
    server.run()
