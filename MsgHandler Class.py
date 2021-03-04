import logging
import os
import sys
import struct
import socket
import time
import datetime
from threading import Thread

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

#Ignore this one############################
class SignalAPI(MsgHandler):
    #Need code that checks to see if message is unread
    with newMSG('TRUE'):
        
        #Load Protobuf Message
    
        #Take decoded message and assign values
    
        #Call the correct Function
        newMSG('False')
    def __init__(self, signal):
        self.signal = signal
        UpdateSystem = "SysUpd" #What value represents these systems in the protobuf
        Webserve = "1"
##################

class MsgHandler:
    def __init__(self, msgType, msgBuff)
        ##Unpack 4bytes to msgtype so we can separate messages
        self.msgType = msgType
        self.msgBuff = msgBuff
            #msgType = struct.unpack('<L', buffType)[0]
        #Set protobuff into necessary structs
            #msgBuff = self.m_Socket.recv(buffSize)
        runMsgHandler(msgType,msgBuff)
        
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
        #System Updates
        else if signal == SYS_UPD:
            msgFromClient.ParseFromString(msgBuff)
            logging.warning("MsgHandler received System Update signal.")
            #Voltage, Current, Temperature, Light Level from sensors/circuit 0-255
            
        #Update
        else if signal == UPDATE:
            msgFromClient.ParseFromString(msgBuff)
            logging.warning("MsgHandler received Update signal.")
            #Light Level, Temperature, Voltage/PWM to EMS
        else:
            logging.error("Received unknown message type")
            
class EmergencyShutdown:
    def __init__(self,value):
        self.value = value
        if self.value = "TRUE"
            from subprocess import call
            call("sudo shutdown -h now", shell=True)
        else:
            
class PowerOnOff:
    def __init__(self,value):
        PWR_ON = 1
        PWR_OFF = 0
        self.value = value
        if value = "PWR_ON":
            #Start Algorithm
            Algorithm(TRUE)
        else if value = "PWR_OFF":
            #Stop Algorithm
            Algorithm(FALSE)
        else:
            Algorithm(FALSE)
        

