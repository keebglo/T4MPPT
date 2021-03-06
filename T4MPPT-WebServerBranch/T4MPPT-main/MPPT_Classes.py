###NOTES###
#Possibility of using SQL table instead of csv file as output to hold our values? -> Probably yes and look into later
#How exactly does our algorithm watch for other pis? -> Reduce the maximum output per Pi. Max voltage per pi = 48/(# of Pi's)
#48V cap for output
#Cap at 3-4 Pi's 

###TO DO###
#Update Message Handler for Webserver
#System Update Handler
#Create Update Function for Algorithm
#Implement structure for child Pi's
#Create a Main function
#Parse Msgbufs in necessary areas for Message Handler (System Update, Emergency Shutdown, Webserver Update)
#EMS Team synchronization??

import logging
import os
import sys
import struct
import socket
import sqlite3 #SQL TABLE IF WE ARE USING INSTEAD OF CSV
import time
import datetime
from threading import Thread
import RPi.GPIO as GPIO
import time
import array as arr
import tcp_server
import ADC_read

import EmergencyMsg_pb2
import UpdateMsg_pb2
import UpdateRequestMsg_pb2
from subprocess import call
import PowerOffMsg_pb2

#Global variables up here
#----------------------------------
# i.e. global m_Gcount
global m_GPowerValue
global m_GVoltageValue
global m_GCurrentValue
global m_GTemperatureValue
#----------------------------------


logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
TRUE = 1

#INITIALIZATION 
class Initialize:

#class variables
    #---------------------------
    # m_cName
    #---------------------------
   
   def __init__(self):
    #Pin and Value sets
        CurrentInputPin = 18    #GPIO 18, Pin 12
        VoltageInputPin = 23    #GPIO 23, Pin 16 
    #VoltageOutputPin = 24  #GPIO 24, Pin 18
        TemperaturePin = 5      #GPIO 5, Pin 29
        IrradiancePin = 6       #GPIO 6, Pin 31
        pwmPin = 32             #GPIO 12 (PWM0), Pin 32
        frequency = 1000   #100Mhz Frequency
        dutycycle = 50          #initial duty cycle of 50
    #Initialization of Classes    
        m = MsgHandler
        a = Algorithm
    #Initialization for RaspberryPi
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pwmPin,GPIO.OUT)
        GPIO.setup(CurrentInputPin, GPIO.IN)
        GPIO.setup(VoltageInputPin, GPIO.IN)
        GPIO.setup(TemperaturePin, GPIO.IN)
        GPIO.setup(IrradiancePin, GPIO.IN)
        global pulse
        pulse = GPIO.PWM(pwmPin, frequency)
        pulse.start(25)
        print("Initialization Complete")
        
        ip = '192.168.0.60'
        port = 10000
        global server
        server = tcp_server.TCPServer(ip, port)
            
#MESSAGE HANDLER
class MsgHandler:
    def __init__(self, msgType, msgBuff):
        ##Unpack 4bytes to msgtype so we can separate messages
        self.msgType = msgType
        self.msgBuff = msgBuff
            #msgType = struct.unpack('<L', buffType)[0]
        #Set protobuff into necessary structs
            #msgBuff = self.m_Socket.recv(buffSize)
        es = EmergencyShutdown
        ponoff = PowerOnOff
        self.runMsgHandler(msgType,msgBuff)
        
    def runMsgHandler(self, signal, signalmsg):
        PWR = 3
        EMG_SD = 1
        SYS_UPD = 4
        MSG_UPD = 5
        EMS = 2
        TRUE = "TRUE"
        self.signal = signal
        self.signalmsg = signalmsg
        #Power On/Power Off
        if signal == PWR:
            #Power on the System Algorithm
            msgFromClient = PowerOffMsg_pb2.PowerOff()
            msgFromClient.ParseFromString(msgBuff)
            #if msgFromClient.PowerSignal == 0
            logging.warning("MsgHandler received Power Off signal")
            self.sendpwr = PowerOnOff(0)
            #else if msgFromClient.PowerSignal == 1
               # logging.warning("MsgHandler received Power On signal")
               # self.sendpwr = PowerOnOff(1)
        #Emergency Shutdown
        elif signal == EMG_SD:
            #Maybe try to save processes before closing
            msgFromClient = EmergencyMsg_pb2.EmergencyShutdown()
            msgFromClient.ParseFromString(msgBuff)
            logging.warning("MsgHandler received Emergency shutdown signal.")
            self.SysShutdown = EmergencyShutdown(TRUE)
        #System Updates from child Pi's
        elif signal == SYS_UPD:
            msgFromClient = UpdateRequestMsg_pb2.UpdateRequest()
            msgFromClient.ParseFromString(msgBuff)
            logging.warning("MsgHandler received System Update signal.")
            #Voltage, Current, Temperature, Light Level from sensors/circuit 0-255
        #Update for Webserver
        elif signal == UPDATE:
            msgFromClient = UpdateMsg_pb2.Update()
            msgFromClient.ParseFromString(msgBuff)
            logging.warning("MsgHandler received Update signal.")
            #Light Level, Temperature, Voltage/PWM to EMS
        elif signal == EMS:
            print("EMS")
        #Unknown Message type received
        else:
            logging.error("Received unknown message type")
            
#EMERGECNY SHUTDOWN FUNCTION
class EmergencyShutdown:
    def __init__(self,value):
        self.value = value
        self.EShutDown(value)
        
    def EShutDown(self,value):
        self.value = value
        if self.value == TRUE:
            print("It turned off")
            #call("sudo shutdown -h now", shell=True)

        
#POWER CONTROL FUNCTION
class PowerOnOff:
    def __init__(self,value):
        PWR_ON = 1
        PWR_OFF = 0
        self.value = value
        self.update(value)
        
    def update(self, value):
        self.value = value
        if value == "PWR_ON":
            #Start Algorithm
            a.signal(TRUE)
        elif value == "PWR_OFF":
            #Stop Algorithm
            a.signal(FALSE)
        else:
            a.signal(FALSE)
            
#ALGORITHM 
class Algorithm():
    def __init__(self):
        value = "FALSE"
        #RunAlgorithm(AlgCheck)
        
        #CurrentValue = arr.array('f', [0,0,0,0,0])
        #RunAlgorithm(value)
    

    def RunAlgorithm(self, signal):
        #Run the Algorithm
        #self.checkAlg = signal
        
        PowerValue = arr.array('f', [0,1,0,1,0])
        print("Power Array Value = ", PowerValue)
        VoltageValue = arr.array('f', [0,0,0,0,0])
        print("Voltage Array Value = ", VoltageValue)    
        print("Algorithm is running...")
        dutycycle = 50
        PowerValue[1] = 1
        
        timer = time.time() * 1000
        
        while(1):
            #currentTime = time.time() * 1000
           # if (timer - currentTime >=5):
                
                server.post()
                #timer = time.time() * 1000
                time.sleep(5)

                
    #Update the variable with value                        
    #def update(var,value):

    #Shifts current Power values down the array to hold previous values
    def PowerValueShift(self):
        for i in range(4):
            PowerValue[i] = PowerValue[i-1]

    #Shifts current Voltage values down the array to hold previous  values
    def VoltageValueShift(self):
        for i in range(4):
            VoltageValue[i] = VoltageValue[i-1]

    #Module to print out values (ONLY IF NOT SQL)
    def PrintValues():
        with open('output.txt','w') as f:
            from datetime import datetime
            now = datetime.now()
            gettime = now.strftime("%H:%M:%S")
            print(gettime)
            print("\n")
            print(VoltagePin, CurrentPin, VoltagePin*CurrentPin, TemperaturePin, IrradiancePin,"\n")
            
 
        
