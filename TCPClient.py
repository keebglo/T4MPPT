import os
import sys
import struct
import socket
import time
import datetime
from threading import Thread

class TCPClient:
    
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
    
  
    
#----------------------------------------------------------------------------
#   Initializations- Create socket connection to server
#----------------------------------------------------------------------------

    def __init__(self):
        try:
            self.m_Socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
            if self.m_Socket is None:
                print("Unable to create socket")
       
             
            else:

                print("Socket Created...")  
                self.m_Socket.connect((self.IP_ADDR, self.PORT))
                print("Socket Connected...")            
                self.m_bRunning = True

                #---------------------------------
                #m_Socket.sendall(b'Hello, world')
                #data = m_Socket.recv(1024)                 Test client- Echo 
                #print('Received', repr(data))
                #---------------------------------
   
                #Display menu to test message sending
                self.__MainMenu()      
            
                #Thread to process receive messages
                self.m_rxThread = Thread (target = self.__processRXMsgs)
                #Process message chosen to send
                self.__MessageSelection()
    
        except Exception as e:
            print(e) 
    #---------------------------------------------------------------------
   
    def __MainMenu(self):
        print("-------------------------------")
        print("Commands:")
        print("-------------------------------")
        print ("    1 : Test Message")
        print ("    X : Close Socket")
        print("-------------------------------")
    
     #---------------------------------------------------------------------
    
    def __MessageSelection(self):
         
         MessageChosen = None
         self.m_rxThread.start()

         while (self.m_bRunning):

             #Wait for input
             MessageChosen = input("> ")

             if not self.m_bRunning: 
                break
                print ("Thread not running")

             if MessageChosen == '1':
                print("Sending Test Message")
                self.__sendMsg1()

             elif (MessageChosen == "X" or MessageChosen == 'x'):
                 print ("Closing Socket")
                 print ("Peace out girl scout <3")
                 self.m_bRunning = False

            #Socket Clean up
         self.m_Socket.close()
         self.m_rxThread.join()
         sys.exit(0)
    
   #---------------------------------------------------------------------
   
    def __sendMsg1(self):
        msg = "1"
        self.m_Socket.sendall(msg.encode())
        print("Message Sent")


    #---------------------------------------------------------------------

    def __processRXMsgs(self):

        data = self.m_Socket.recv(1024)                 
        print('Received', repr(data))

    #---------------------------------------------------------------------

if __name__ == "__main__":
    server = TCPClient()