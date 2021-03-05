import socket
import sys


class StubClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 10000)
        print("client created with server address {} and port {}".format(
            self.server_address[0], self.server_address[1]))

    def connect(self):
        print("attempting to connect to {} on port {}.".format(
            self.server_address[0], self.server_address[1]))
        try:
            self.sock.connect(self.server_address)
            print("connection successful")
        except Exception as e:
            print("connection failed")
            print(e)

    def post(self):
        try:
            message = b"hello from the client"
            print("sending:  {}".format(message))
            self.sock.sendall(message)

            amount_recieved = 0
            amount_expected = len(message)

            while amount_recieved < amount_expected:
                data = self.sock.recv(16)
                amount_recieved += len(data)
                print("recieved: {}".format(data))

        finally:
            print("closing client socket")
            self.sock.close()



if __name__ == "__main__":
    client = StubClient()
    client.connect()
    client.post()