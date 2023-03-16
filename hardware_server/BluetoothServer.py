import struct
import threading
from queue import Queue
from collections import deque

import bluetooth
from bluetooth import BluetoothError

from hardware_server import Packet
from hardware_server.Header import Header


class Bluetooth:
    """
    Establishes a bluetooth connection and sends data
    """

    UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    def __init__(self):
        self._connected = True
        self.send_queue = Queue()
        self.receive_queue = deque()
        self.receive_lock = threading.Lock()

    def _send_thread(self, socket):
        """
        Sends data from the send queue to the client.
        :return:
        """
        while self._connected:
            if not self.send_queue.empty():
                data_type, data = self.send_queue.get()
                packet_bytes = Packet.as_bytes(False, False, data_type, data)

                try:
                    socket.send(packet_bytes)
                except BluetoothError:
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
            data = struct.unpack("!ii", data_bytes)

            with self.receive_lock:
                self.receive_queue.append(data)
        except BluetoothError:
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
        self._sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self._sock.bind(("", bluetooth.PORT_ANY))
        self._sock.listen(1)
        port = self._sock.getsockname()[1]

        bluetooth.advertise_service(self._sock, "SampleServer", service_id=self.UUID,
                                    service_classes=[self.UUID, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])

        print("Waiting for connection on RFCOMM channel", port)
        client_sock, client_info = self._sock.accept()
        self._connected = True
        self.send_queue = Queue()
        self.receive_queue = deque()
        return client_sock

    def run(self):
        """
        Attempts sending/receiving data through the thread. Attempts reconnection upon error
        :return:
        """
        while True:
            client_sock = self.initialise_connection()

            # Attempt sending/receiving
            send_thread = threading.Thread(target=self._send_thread, args=(client_sock,))
            receive_thread = threading.Thread(target=self._receive_thread, args=(client_sock,))

            # Start threads
            send_thread.start()
            receive_thread.start()

            send_thread.join()
            receive_thread.join()

            client_sock.close()
            self._sock.close()


if __name__ == "__main__":
    server = Bluetooth()
    server.run()
