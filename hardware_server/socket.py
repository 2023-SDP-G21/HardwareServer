import socket
import threading
from queue import Queue

SERVER_ADDRESS = "localhost"
SERVER_PORT = 3000


def receive_thread(sock, receiving_queue):
    while True:
        data = sock.recv(1024)
        receiving_queue.put(data.decode())


def send_thread(sock, sending_queue):
    while True:
        if not send_queue.empty():
            message = sending_queue.get()
            sock.sendall(message.encode())


def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_details = (SERVER_ADDRESS, SERVER_PORT)
    sock.bind(connection_details)
    return sock


def monitor_connection(sending, receiving):
    # Send sensor data and warnings
    while True:
        if not receiving.empty():
            # TODO : Process received Data
            print("Received: ", receive_queue.get())

        # TODO : Collect and process data from sensors on Raspberry Pi

        # TODO : Send data from sensors to software backend

        # TODO : Send warnings to software backend


if __name__ == "__main__":
    # Create a socket and listen for connections
    socket = create_socket()
    socket.listen(1)
    print("Waiting for a connection...")
    connection, client_address = socket.accept()
    print("Connection from", client_address)

    # Initialise queues and threads for sending and receiving data
    send_queue = Queue()
    receive_queue = Queue()
    receive_thread = threading.Thread(target=receive_thread, args=(connection, receive_queue))
    receive_thread.start()
    send_thread = threading.Thread(target=send_thread, args=(connection, send_queue))
    send_thread.start()
    monitor_connection(send_queue, receive_queue)
