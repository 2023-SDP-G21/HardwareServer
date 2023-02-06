import socket


class TCP:
    __socket = None
    __ip = "localhost"
    __port = 3000

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__ip, self.__port))

    def send(self, client, data):
        client.send(data)
    def run(self):
        self.__socket.listen(1)
        print("Waiting for a connection...")
        connection, client_address = self.__socket.accept()
        print("Connection from", client_address)

        # while true -


if __name__ == "__main__":
    server = TCP()
    server.run()
