import socket
import sys


class StubServer:
    def __init__(self):
        # Create TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 10000)
        print("starting up on {} port {}".format(
            server_address[0], server_address[1]))

        # Bind the socket to the port
        sock.bind(server_address)

        sock.listen(1)

        while True:
            print("waiting for connection")
            connection, client_address = sock.accept()
            try:
                print("connection from {}".format(client_address))

                while True:
                    data = connection.recv(16)
                    print("recieved: {}".format(data))

                    if data:
                        print("sending data back to the client")
                        connection.sendall(data)
                    else:
                        print("nore data from {}".format(client_address))
                        break

            finally:
                connection.close()

if __name__ == "__main__":
    server = StubServer()
    