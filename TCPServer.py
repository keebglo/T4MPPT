import os
import sys
import struct
import socket
import time
import datetime
from threading import Thread

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
                
                    self.m_ClientConnection, self.m_addr = self.m_Socket.accept()
                    self.m_bRunning = True
    
                    with self.m_ClientConnection:
                        print('Connected by', self.m_addr)
                        while True:
                            data = self.m_ClientConnection.recv(1024).decode()
                            print(data)

                            if data == '1':
                                self.m_ClientConnection.sendall(b'Test Message Received')
                        #Thread to process incoming messages
                            #self.m_rxThread = Thread(target=self.__processRXMsgs)
                  
                       # elif data == 'Test Message':
                           # conn.sendall('Test Message Received')

                    

            except Exception as e:
                print(e)

        except Exception as e:
            print("Problem in init")
#-------------------------------------------------------------------------------------------

    def __processRXMsgs(self):


        self.m_rxThread.start()

        while (self.m_bRunning):
            data = self.m_ClientConnection.recv(1024)
            print(data)

            if data == 'Test Message':
                self.m_ClientConnection.sendall('Test Message Received')

            else:
               self.m_bRunning = False

        self.m_Socket.close()
        self.m_rxThread.join()
        sys.exit(0)

if __name__ == "__main__":
    server = TCPSever()