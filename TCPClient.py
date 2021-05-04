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
    m_inputVoltage = None
    m_outputVoltage = None
    m_inputCurrent = None
    m_outputCurrent = None
    m_irradiance = None
    m_temperature = None

    
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

                        self.m_timeTag = msgFromServer.TimeTag
                        self.m_inputVoltage = msgFromServer.inputVoltage
                        self.m_outputVoltage = msgFromServer.outputVoltage
                        self.m_inputCurrent = msgFromServer.inputCurrent
                        self.m_outputCurrent = msgFromServer.outputCurrent
                        self.m_irradiance = msgFromServer.irradiance
                        self.m_temperature = msgFromServer.temperature
                              
                        self.writeToCSV()
                        
                        print("Message Received")
                        
                        
                        time_formatted = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(self.m_timeTag/1000))
                        print("Time tag", time_formatted)
                        print("Input Voltage: ", self.m_inputVoltage)
                        print("Input Current: ", self.m_outputVoltage)
                        print("Output Voltage: ", self.m_inputCurrent)
                        print("Output Current: ", self.m_outputCurrent)
                        print("Temperature: ", self.m_temperature)
                        print("Irradiance: ", self.m_irradiance)
                        
                        

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

        
    def writeToCSV(self):
        filePath = '/var/www/html' 
        fileName = 'ConverterValues.txt'
        fullPath = os.path.join(filePath, fileName)
        
        time_formatted = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(self.m_timeTag/1000))
        
        file = open(fullPath, "a")
        file.write(time_formatted)
        file.write(',')
        file.write(self.m_inputVoltage)
        file.write(',')
        file.write(self.m_outputVoltage)
        file.write(',')
        file.write(self.m_inputCurrent)
        file.write(',')
        file.write(self.m_outputCurrent)
        file.write(',')
        file.write(self.m_temperature)
        file.write(',')
        file.write(self.m_irradiance)
        file.write('\n')

        file.close()
    #---------------------------------------------------------------------

if __name__ == "__main__":
    server = TCPClient()