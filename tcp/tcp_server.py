import os 
import sys
import struct
import socket
import time
import datetime
import threading

from lib import EmergencyMsg_pb2, PowerOffMsg_pb2, UpdateMsg_pb2, UpdateRequestMsg_pb2


class TCPServer:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

        self.make_socket()
        self.listen()
        
    
    def make_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.ip_address, self.port))
            if self.sock is None:
                print("unable to create socket")
            else:
                print("server created socket at {}".format(self.port))
        except socket.error as e:
            print(e)

    def listen(self):
        try:
            self.sock.listen(1)
            print("server listening ...")
            while True:
                connection, client_address = self.sock.accept()
                print("Connected by {}".format(client_address))  
                
                msg_size_from_packet_buff = connection.recv(4)
                msg_type_from_packet_buff = connection.recv(4)
                
                msg_size = struct.unpack('<L', msg_size_from_packet_buff)[0]
                msg_type = struct.unpack('<L', msg_type_from_packet_buff)[0]
                actual_msg = connection.recv(msg_size)

                self.decode_message(msg_size, msg_type, actual_msg)

        except Exception as e:
            print(e)


    def decode_message(self, msg_size,msg_type, actual_msg):
        if msg_size > 0:
            if msg_type == 1:
                self.decode_Emergency2Msg_pb2(actual_msg)
                

    def decode_Emergency2Msg_pb2(self, actual_msg):
            print("Emergency message received")
            msg_from_client = EmergencyMsg_pb2.EmergencyShutdown()
            msg_from_client.ParseFromString(actual_msg)
            print("Timetag: ", msg_from_client.TimeTag)
            print("Message: ", msg_from_client.emergencyMsg)
            print("Problem: ", msg_from_client.problem)


if __name__ == "__main__":
    ip = 'localhost'
    port = 10000
    server = TCPServer(ip, port)

    