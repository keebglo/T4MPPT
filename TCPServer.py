import os
import sys
import struct
import socket
import time
import datetime
from threading import Thread


 #-------------
 # Protobuf Files
 #--------------
import lib.EmergencyMsg_pb2 
import lib.PowerOffMsg_pb2 
import lib.UpdateMsg_pb2
import lib.UpdateRequestMsg_pb2

class TCPSever:
 #-------------
    # Class Constants
    #--------------
    
    IP_ADDR = '127.0.0.1'
    PORT = 11001
    
    #-------------------
    # Class Memeber Variables
    #------------------
    
    m_bRunning = False
    m_Socket = None
    m_rxThread = None
    m_ClientConnection = None
    m_addr = None
    
   
#----------------------------------------------------------------------------
#   Initializations- Create socket 
#----------------------------------------------------------------------------

    def __init__(self):
        try:
            self.m_Socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.m_Socket is None:
             print("Unable to create socket")
        
            print("Socket Created...")

            try: 
                self.m_Socket.bind((self.IP_ADDR, self.PORT))
                
                self.m_Socket.listen()
                while True:
                    print("Socket Listening....")
                
                    self.m_Socket, self.m_addr = self.m_Socket.accept()
                    self.m_bRunning = True
    
                    with self.m_Socket:
                        print('Connected by', self.m_addr)
                        while True:
                          
                           sizeBuff = self.m_Socket.recv(4)

                           sizeInfo = struct.unpack('<L', sizeBuff)[0]

                           if sizeInfo > 0:
                                      #unpack 4 bytes (Little Endian)
                                      buffType = self.m_Socket.recv(4)
                                      msgType = struct.unpack('<L', buffType)[0]

                                      #process proto message
                                      msgBuff = self.m_Socket.recv(sizeInfo)

                                      if msgType == 1:
                                          print("---> Emergency Message Received")
                                          msgFromClient = lib.EmergencyMsg_pb2.EmergencyShutdown()
                                          msgFromClient.ParseFromString(msgBuff)

                                          print("Timetag: ", msgFromClient.TimeTag)
                                          print("Message: ", msgFromClient.emergencyMsg)
                                          print("Problem: ", msgFromClient.problem)


                    

            except Exception as e:
                print(e)

        except Exception as e:
            print("Problem in init")
#-------------------------------------------------------------------------------------------

  


if __name__ == "__main__":
    server = TCPSever()