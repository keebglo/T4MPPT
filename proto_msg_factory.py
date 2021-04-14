import struct
import time
from abc import ABCMeta, abstractmethod

import EmergencyMsg_pb2
import EMSUpdate_pb2
import PowerOffMsg_pb2
import UpdateMsg_pb2
import UpdateRequestMsg_pb2



class ProtoMsg:
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_string(self):
        pass

    def get_packed_msg(self, msg, msg_type):
        msg_as_bytes = msg.SerializeToString()
        msg_size = len(msg_as_bytes)

        packed_message = (struct.pack('<LL', msg_size, msg_type), msg_as_bytes)
        return packed_message

    def get_time(self):
        return int(time.time() * 1000)

    @staticmethod
    def hang_up():
        return (struct.pack('<LL', 999, 999))


class EmergencyMsg(ProtoMsg):
    def __init__(self):
        self.msg = EmergencyMsg_pb2.EmergencyShutdown()
        self.msg.TimeTag = super().get_time()
        self.msg_type = 1
        self.msg.emergencyMsg = "System Failure"
        self.msg.problem = "Something broke"

    def get_packed_msg(self):
        return super().get_packed_msg(self.msg, self.msg_type)

    def to_string(self):
        print("Emergency Message")
        print("msg type: ", self.msg_type)
        print("time tag: ", self.msg.TimeTag)
        print("emergency message: ", self.msg.emergencyMsg)
        print("problem: ", self.msg.problem)


class EMSUpdate(ProtoMsg):
    def __init__(self):
        self.msg = EMSUpdate_pb2.EMSUpdate()
        self.msg.TimeTag = super().get_time()
        self.msg_type = 2
        self.msg.load = "load"
        self.msg.LoadValue = 3

    def get_packed_msg(self):
        return super().get_packed_msg(self.msg, self.msg_type)

    def to_string(self):
        print("EMS Update Message")
        print("msg type: ", self.msg_type)
        print("time tag: ", self.msg.TimeTag)
        print("load: ", self.msg.load)
        print("load value: ", self.msg.LoadValue)


class PowerOff(ProtoMsg):
    def __init__(self):
        self.msg = PowerOffMsg_pb2.PowerOff()
        self.msg.TimeTag = super().get_time()
        self.msg_type = 3
        self.msg.powerOff = "power off"

    def get_packed_msg(self):
        return super().get_packed_msg(self.msg, self.msg_type)

    def to_string(self):
        print("Power off message")
        print("msg type: ", self.msg_type)
        print("time tag: ", self.msg.TimeTag)
        print("message: ", self.msg.powerOff)


class UpdateRequest(ProtoMsg):
    def __init__(self):
        self.msg = UpdateRequestMsg_pb2.UpdateRequest()
        self.msg.TimeTag = super().get_time()
        self.msg_type = 4
        self.msg.request = "making request"

    def get_packed_msg(self):
        return super().get_packed_msg(self.msg, self.msg_type)

    def to_string(self):
        print("Update Request Message")
        print("msg type: ", self.msg_type)
        print("Time tag: ", self.msg.TimeTag)
        print("Request: ", self.msg.request)


class UpdateMsg(ProtoMsg):
    def __init__(self):
        self.msg = UpdateMsg_pb2.Update()
        self.msg.TimeTag = super().get_time()
        self.msg_type = 5
        self.msg.current = 111
        self.msg.voltage = 222
        self.msg.temperature = 333
        self.msg.irradiance = 444

    def get_packed_msg(self):
        return super().get_packed_msg(self.msg, self.msg_type)

    def to_string(self):
        print("Update Message")
        print("msg type: ", self.msg_type)
        print("Time tag", self.msg.TimeTag)
        print("current: ", self.msg.current)
        print("voltage: ", self.msg.voltage)
        print("temperature: ", self.msg.temperature)
        print("irradiance: ", self.msg.irradiance)