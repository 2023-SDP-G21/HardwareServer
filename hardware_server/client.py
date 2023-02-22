import socket
import struct
import time
import random

if __name__ == '__main__':
    HOST = "localhost"
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            angle = random.randint(-180, 180)
            power = random.randint(0, 100)
            data = struct.pack("!ii", angle, power)
            data_bytes = struct.pack("!??BB", True, False, 1, len(data)) + data
            s.sendall(data_bytes)
            time.sleep(0.05)
