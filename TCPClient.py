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
    IP_ADDR = '192.168.0.60'
    PORT = 10000
    
    #-------------------
    # Class Memeber Variables
    #------------------
    
    m_bRunning = False
    m_Socket = None
    m_rxThread = None
    m_timeTag = 0
    m_inputVoltage = 0
    m_outputVoltage = 0
    m_inputCurrent = 0
    m_outputCurrent = 0
    m_irradiance = 0
    m_temperature = 0

    
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
               
            while(1):   
                sizeBuff = self.m_Socket.recv(4)

                sizeInfo = struct.unpack('<L', sizeBuff)[0]

                if sizeInfo > 0:
                #unpack 4 bytes (Little Endian)
                    buffType = self.m_Socket.recv(4)
                    msgType = struct.unpack('<L', buffType)[0]

                    #process proto message
                    msgBuff = self.m_Socket.recv(sizeInfo)


                    if msgType == 5 :
                        print ("---> Update Message Received")
                        msgFromServer = UpdateMsg_pb2.Update()
                        msgFromServer.ParseFromString(msgBuff)

                        m_timeTag = msgFromServer.TimeTag
                        m_inputVoltage = msgFromServer.current
                        m_outputVoltage = msgFromServer.voltage
                        m_inputCurrent = 0
                        m_outputCurrent = 0
                        m_irradiance = msgFromServer.irradiance
                        m_temperature = msgFromServer.temperature
                              
                        self.writeToCSV()

                        print("Time tag", msgFromServer.TimeTag)
                        print("current: ", msgFromServer.current)
                        print("voltage: ", msgFromServer.voltage)
                        print("temperature: ", msgFromServer.temperature)
                        print("irradiance: ", msgFromServer.irradiance)

                #Thread to process receive messages
                #self.m_rxThread = Thread (target = self.__processRXMsgs)
                
        except Exception as e:
            print(e) 
    #---------------------------------------------------------------------
   


   #---------------------------------------------------------------------
   
    def __sendUpdateRequest(self):
     
       timetag = time.time() * 1000
       iTimeTag = int(timetag)

       msgTosend = UpdateRequestMsg_pb2.UpdateRequest()
       msgTosend.TimeTag = iTimeTag
       msgTosend.request = "True"
 
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
        print("In the thread")
        
        while(self.m_bRunning):
            print("RCV Thread: Waiting for data...")

            sizeBuff = self.m_Socket.recv(4)

            sizeInfo = struct.unpack('<L', sizeBuff)[0]

            if sizeInfo > 0:
            #unpack 4 bytes (Little Endian)
                buffType = self.m_Socket.recv(4)
                msgType = struct.unpack('<L', buffType)[0]

                #process proto message
                msgBuff = self.m_Socket.recv(sizeInfo)


                if msgType == 5 :
                    print ("---> Update Message Received")
                    msgFromServer = UpdateMsg_pb2.Update()
                    msgFromServer.ParseFromString(msgBuff)

                    self.m_timeTag = msgFromServer.TimeTag
                    self. m_inputVotage = msgFromServer.current
                    self.m_outputVoltage = msgFromServer.voltage
                    self.m_inputcurrent = 0
                    self.m_outputcurrent = 0
                    self.m_irradiance = msgFromServer.irradiance
                    self.m_temperature = msgFromServer.temperature
                          
                    writeToCSV()

                    print("Time tag", msgFromServer.TimeTag)
                    print("current: ", msgFromServer.current)
                    print("voltage: ", msgFromServer.voltage)
                    print("temperature: ", msgFromServer.temperature)
                    print("irradiance: ", msgFromServer.irradiance)
        
    def writeToCSV(self):
        filePath = '/var/www/html' #change to location of pi storage
        fileName = 'ConverterValues.txt'
        fullPath = os.path.join(filePath, fileName)

        print("Attempting to write")
        
        file = open(fullPath, "a")
        file.write(str(self.m_timeTag))
        file.write(',')
        file.write(str(self.m_inputVoltage))
        file.write(',')
        file.write(str(self.m_outputVoltage))
        file.write(',')
        file.write(str(self.m_inputCurrent))
        file.write(',')
        file.write(str(self.m_outputCurrent))
        file.write(',')
        file.write(str(self.m_temperature))
        file.write(',')
        file.write(str(self.m_irradiance))
        file.write('\n')

        file.close()
    #---------------------------------------------------------------------

if __name__ == "__main__":
    server = TCPClient()