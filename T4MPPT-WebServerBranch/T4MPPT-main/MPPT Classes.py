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

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
GPIO.setmode(GPIO.BCM)

timer = 0

#INITIALIZATION 
class Initialize:
    def __init__()
    #Pin and Value sets
        CurrentInputPin = 18	#GPIO 18, Pin 12
        VoltageInputPin = 23	#GPIO 23, Pin 16 
        #VoltageOutputPin = 24	#GPIO 24, Pin 18
        TemperaturePin = 5		#GPIO 5, Pin 29
        IrradiancePin = 6		#GPIO 6, Pin 31
        pwmPin = 32				#GPIO 12 (PWM0), Pin 32
        frequency = 100000000   #100Mhz Frequency
        dutycycle = 50          #initial duty cycle of 50
    #Initialization of Classes    
        m = MsgHandler
        a = Algorithm
    #Initialization for RaspberryPi
        GPIO.setup(CurrentInputPin, GPIO.IN)
        GPIO.setup(VoltageInputPin, GPIO.IN)
        GPIO.setup(TemperaturePin, GPIO.IN)
        GPIO.setup(IrradiancePin, GPIO.IN)
        pulse = GPIO.PWM(pwmPin, frequency)
        pulse.start(25)
        
#MESSAGE HANDLER
class MsgHandler:
    def __init__(self, msgType, msgBuff)
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
        PWR = 4
        EMG_SD = 1
        SYS_UPD = 2
        MSG_UPD = 3
        self.signal = signal
        self.signalmsg = signalmsg
        #Power On/Power Off
        if signal == PWR:
            #Power on the System Algorithm
            msgFromClient.ParseFromString(msgBuff)
            if msgFromClient.PowerSignal = 0
                logging.warning("MsgHandler received Power Off signal")
                self.sendpwr = PowerOnOff(0)
            else if msgFromClient.PowerSignal = 1
                logging.warning("MsgHandler received Power On signal")
                self.sendpwr = PowerOnOff(1)
        #Emergency Shutdown
        else if signal == EMG_SD:
            #Maybe try to save processes before closing
            msgFromClient.ParseFromString(msgBuff)
            logging.warning("MsgHandler received Emergency shutdown signal.")
            self.SysShutdown = EmergencyShutdown(TRUE)
        #System Updates from child Pi's
        else if signal == SYS_UPD:
            msgFromClient.ParseFromString(msgBuff)
            logging.warning("MsgHandler received System Update signal.")
            #Voltage, Current, Temperature, Light Level from sensors/circuit 0-255
        #Update for Webserver
        else if signal == UPDATE:
            msgFromClient.ParseFromString(msgBuff)
            logging.warning("MsgHandler received Update signal.")
            #Light Level, Temperature, Voltage/PWM to EMS
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
        if self.value = 'TRUE'
            from subprocess import call
            call("sudo shutdown -h now", shell=True)
        else:
        
#POWER CONTROL FUNCTION
class PowerOnOff:
    def __init__(self,value):
        PWR_ON = 1
        PWR_OFF = 0
        self.value = value
        self.update(value)
        
    def update(self, value)
        self.value = value
        if value = 'PWR_ON':
            #Start Algorithm
            a.signal(TRUE)
        else if value = 'PWR_OFF':
            #Stop Algorithm
            a.signal(FALSE)
        else:
            a.signal(FALSE)
            
#ALGORITHM 
class Algorithm(value):
    def __init__(self, value):
        TRUE = 1
        FALSE = 0
        self.AlgCheck = value
        RunAlgorithm(AlgCheck)
        PowerValue = arr.array(i, [0,0,0,0,0])
        VoltageValue = arr.array(i, [0,0,0,0,0])
        CurrentValue = arr.array(i, [0,0,0,0,0])
        self.RunAlgorithm(value)
        
        
       
    def RunAlgorithm(self, signal)
        #Run the Algorithm
        #self.checkAlg = signal
        timer = time.time() * 1000
        while(1):
        currentTime = time.time() * 1000
            if (timer - currentTime >=5):
                ldr_value = readadc(0)
                
                timetag = time.time() * 1000
                iTimeTag = int(timetag)

                msgTosend = UpdateMsg_pb2.Update()
                msgTosend.TimeTag = iTimeTag
                msgTosend.current = 111
                msgTosend.voltage = 222
                msgTosend.irradiance = ldr_value
                msgTosend.temperature = 3333
       
                msgBytestoSend = msgTosend.SerializeToString()
                payloadsize= len(msgBytestoSend)
                sizeinfo = struct.pack('<L', payloadsize)
                msgType = 5
                msgTypeInfo = struct.pack('<L', msgType)

                print ("Message sent:")
                print ("Size Info: ", sizeinfo)
                print ("Msg Type: ", msgType)
                print ("Message: ", msgBytestoSend)

                TCPServer.sock.send(sizeinfo + msgTypeInfo + msgBytestoSend)
        
            '''while(signal == TRUE):
                if PowerValue[0] != PowerValue[1]
                    if PowerValue[0] > PowerValue[1] #If latest power value is greater than the previous value
                        #If PV_v(n) > PV_v(n-1)
                        if VoltageValue[0] > VoltageValue[1] #If most recent voltage value is greater than the previous value, the duty cycle decreases
                            dutycycle -= 5
                            pulse.ChangeDutyCycle(dutycycle)
                        #If PV(n) < PV(n-1)
                        else #If most recent voltage value is less than the previous value, the duty cycle increases
                            //Increase PWM
                            dutycycle += 5
                            pulse.ChangeDutyCycle(dutycycle)
                    else #If latest power value is less than the previous value
                        #If PV_v(n) > PV_v(n-1)
                        if VoltageValue[0] > VoltageValue[1] #If most recent voltage value is greater than the previous value, the duty cycle increases
                            #Increase PWM
                            dutycycle += 5
                            pulse.ChangeDutyCycle(dutycycle)
                        #If PV(n) < PV(n-1)
                        else #If most recent voltage value is less than the previous value, the duty cycle decreases
                            //Decrease PWM
                            dutycycle -= 5
                            pulse.ChangeDutyCycle(dutycycle)
                time.sleep(60)#60 second wait '''
                
    #Update the variable with value                        
    def update(var,value)

    #Shifts current Power values down the array to hold previous values
    def PowerValueShift():
        for i in range(4)
            PowerValue[i] = PowerValue[i-1]

    #Shifts current Voltage values down the array to hold previous  values
    def VoltageValueShift():
        for i in range(4)
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
            
 
     def sendMsg():
         
        
