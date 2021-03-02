import os
import sys
import struct
import socket
import time
import datetime
from threading import Thread


#---------------------------
#Proto Files
#---------------------------
import EmergencyMsg_pb2
import UpdateMsg_pb2
import UpdateRequestMsg_pb2
import PowerOffMsg_pb2 


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
                self.__sendEmergencyMsg()

             elif (MessageChosen == "X" or MessageChosen == 'x'):
                 print ("Closing Socket")
                 print ("Peace out girl scout <3")
                 self.m_bRunning = False

            #Socket Clean up
         self.m_Socket.close()
         self.m_rxThread.join()
         sys.exit(0)
    
   #---------------------------------------------------------------------
   
    def __sendEmergencyMsg(self):
        #msg = "1"
       # self.m_Socket.sendall(msg.encode())        Test code
        #print("Message Sent")

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

       self.m_Socket.send(sizeinfo + msgTypeInfo + msgBytestoSend)

    #---------------------------------------------------------------------

    def __processRXMsgs(self):

        bServerDisconnect = False

        while(self.m_bRunning):
            print("RCV Thread: Waiting for data...")
            
            #4 bytes from buffSize
            buffSize = self.m_Socket.recv(4)          
            
            #server disconnect
            if len(buffSize) == 0:
                bServerDisconnect = True
                break

            else:
                buffSize = struct.unpack('<L', buffSize)[0]

                if buffSize > 0:
                    #unpack 4 bytes (little endian)
                    buffType = self.m_Socket.recv(4)
                    msgType = struct.unpack('<L', buffType)[0]

                    #process proto message
                    msgBuff = self.m_Socket.recv(buffSize)

                    if msgType == 1 :
                        print ("---> Emergency Message Received")
                        msgFromSever = EmergencyMsg_pb2.EmergencyShutdown()
                        msgFromServer.ParseFromString(msgBuff)

                        print("Timetag: ", msgFromServer.TimeTag)
                        print("Message: ", msgFromServer.emergencyMsg)
                        print("Problem: ", msgFromServer.problem)

        
                   # data self.m_Socket(1024)
                   # print('Received', repr(data))      Test code

    #---------------------------------------------------------------------

if __name__ == "__main__":
    server = TCPClient()