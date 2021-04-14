import struct
import socket
import threading
import ADC_read
import time

import EmergencyMsg_pb2
import EMSUpdate_pb2
import PowerOffMsg_pb2
import UpdateMsg_pb2
import UpdateRequestMsg_pb2



class TCPServer:
    webSock = None
    webAddr= None
 
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.alreadyrunning = 0
        self.make_socket()
        self.listen()

    def make_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.ip_address, self.port))
            if self.sock is None:
                print("unable to create socket")
            else:
                print("server created socket at {}".format(self.port))
        except socket.error as e:
            print(e)
            alreadyrunning = 1
            print(alreadyrunning)
            exit

    def listen(self):
        #while True:
            self.sock.listen(1)
            self.webSock, self.webAddr = self.sock.accept()
            #global clientnumreturn
            #clientnumreturn += 1
            #newthread = ClientThread(clientAddress, clientsock)
            newthread = ClientThread(self.webAddr, self.webSock)
            newthread.start()
    
    def post(self):
        #try:
         #   self.sock.send(msg[0] + msg[1])
        #except Exception as e:
         #   print(e)
                ldr_value = ADC_read.readadc(0)
                inputVoltage= ADC_read.readadc(1)
                
                print ("LDR Value: ", ldr_value)
                timetag = time.time() * 1000
                iTimeTag = int(timetag)
                
                print("Input Voltage Value: ", inputVoltage)
                iTimeTag1= int(timetag)

                msgTosend = UpdateMsg_pb2.Update()
                msgTosend.TimeTag = iTimeTag
                msgTosend.current = 111
                msgTosend.voltage = inputVoltage
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

                self.webSock.send(sizeinfo + msgTypeInfo + msgBytestoSend)

class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.csocket = client_socket
        self.client_address = client_address
        print("New connection added: ", self.client_address)
        #print("    Client#",clientnum)

    def run(self):
        try:
            print("connection from: ", self.client_address)
            while True:
                msg_size_from_packet_buff = self.csocket.recv(4)
                msg_type_from_packet_buff = self.csocket.recv(4)

                msg_size = struct.unpack('<L', msg_size_from_packet_buff)[0]
                msg_type = struct.unpack('<L', msg_type_from_packet_buff)[0]

                if msg_type == 999:
                    break

                actual_msg = self.csocket.recv(msg_size)
                self.decode_message(msg_size, msg_type, actual_msg)

            print("client at ", self.client_address, "disconnected ...")
        except Exception as e:
            print(e)


    def decode_message(self, msg_size, msg_type, actual_msg):
        if msg_size > 0:
            if msg_type == 1:
                Decoder.decode_EmergencyMsg(actual_msg)
            elif msg_type == 2:
                Decoder.decode_EMSUpdate(actual_msg)
            elif msg_type == 3:
                Decoder.decode_PowerOff(actual_msg)
            elif msg_type == 4:
                Decoder.decode_UpdateRequest(actual_msg)
            elif msg_type == 5:
                Decoder.decode_UpdateMsg(actual_msg)
                
                
    

class Decoder:
    @staticmethod
    def decode_EmergencyMsg(actual_msg):
        msg_from_client = EmergencyMsg_pb2.EmergencyShutdown()
        msg_from_client.ParseFromString(actual_msg)
        print("Emergency message received")
        print("Timetag: ", msg_from_client.TimeTag)
        print("Message: ", msg_from_client.emergencyMsg)
        print("Problem: ", msg_from_client.problem)

    @staticmethod
    def decode_EMSUpdate(msg):
        decoded_msg = EMSUpdate_pb2.EMSUpdate()
        decoded_msg.ParseFromString(msg)
        print("EMS Update Recieved")
        print("Time Tag: ", decoded_msg.TimeTag)
        print("load: ", decoded_msg.load)
        print("load value: ", decoded_msg.LoadValue)

    @staticmethod
    def decode_PowerOff(msg):
        decoded_msg = PowerOffMsg_pb2.PowerOff()
        decoded_msg.ParseFromString(msg)
        print("Power Off Received")
        print("Time tag: ", decoded_msg.TimeTag)
        print("message: ", decoded_msg.powerOff)

    @staticmethod
    def decode_UpdateRequest(msg):
        decoded_msg = UpdateRequestMsg_pb2.UpdateRequest()
        decoded_msg.ParseFromString(msg)
        print("Update Request Received")
        print("Time tag: ", decoded_msg.TimeTag)
        print("Request: ", decoded_msg.request)

    @staticmethod
    def decode_UpdateMsg(msg):
        decoded_msg = UpdateMsg_pb2.Update()
        decoded_msg.ParseFromString(msg)
        print("Update Message Recieved")
        print("Time tag: ", decoded_msg.TimeTag)
        print("current: ", decoded_msg.current)
        print("voltage: ", decoded_msg.voltage)
        print("temperature: ", decoded_msg.temperature)
        print("irradiance: ", decoded_msg.irradiance)


if __name__ == "__main__":
    ip = 'localhost'
    port = 10000
    server = TCPServer(ip, port)
