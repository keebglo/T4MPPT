import time
import socket
import sys
import struct

from lib import EmergencyMsg_pb2, PowerOffMsg_pb2, UpdateMsg_pb2, UpdateRequestMsg_pb2


class TCPClient:
    def __init__(self, address):
        self.ip_address = address
        self._print_msg("client created with")
        self._make_socket()
        self._connect()


    def _make_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.sock is None:
                print("client socket not created")
            else:
                print("client socket created")
        except socket.error as e:
            print(e)
        
      
    def _connect(self):
        self._print_msg("attempting to connect to")
        try:
            self.sock.connect(self.ip_address)
            print("connection successful")
        except Exception as e:
            print("Connection failed with: ")
            print(e)

    
    def post(self):
        try:
            timetag = time.time() * 1000
            iTimeTag = int(timetag)

            msgTosend = EmergencyMsg_pb2.EmergencyShutdown()
            msgTosend.TimeTag = iTimeTag
            msgTosend.emergencyMsg = "System Failure"
            msgTosend.problem = "Something broke"
            
            msgBytestoSend = msgTosend.SerializeToString()
            
            payloadsize= len(msgBytestoSend)
            sizeinfo = struct.pack('<L', payloadsize)
            msgType = 1
            msgTypeInfo = struct.pack('<L', msgType)

            print ("Message sent:")
            print ("Size Info: ", sizeinfo)
            print ("Msg Type: ", msgType)
            print ("Message: ", msgBytestoSend)

            self.sock.send(sizeinfo + msgTypeInfo + msgBytestoSend)
        except Exception as e:
            print(e)

    def _print_msg(self, message):
        print(message + " server {} on port {}".format(self.ip_address[0], self.ip_address[1]))

    

