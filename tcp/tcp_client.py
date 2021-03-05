import time
import socket
import sys


class ProtoMsg:
    def __init__(self, message):
        self.msg = message


class TCPClient:
    def __init__(self, address, port):
        self.address = address
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._print_msg("client created with")
        
        # self._connect()
      
    def _connect(self):
        self._print_msg("attempting to connect to")
        try:
            self.sock.connect(self.address)
            print("connection successful")
        except Exception as e:
            print("Connection failed with: ")
            print(e)

    #TODO: refactor message creation out of tcp client
    def post(self, msg):
        """Sends message to TCP server"""
        return "posted: " + msg
       
        
        

    def _print_msg(self, message):
        print(message + " server {} on port {}".format(self.address, self.port))

