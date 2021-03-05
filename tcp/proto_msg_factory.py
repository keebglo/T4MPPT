import time
import struct

from lib import EmergencyMsg_pb2, EMSUpdate_pb2, PowerOffMsg_pb2, UpdateMsg_pb2, UpdateRequestMsg_pb2


class ProtoMsgFactory:
    def __init__(self):
        pass

    @staticmethod
    def pack_msg(msg):
        msg_as_bytes = msg.SerializeToString()
        msg_size = len(msg_as_bytes)
        msg_size_info = struct.pack('<L', msg_size)
        msg_type = 1
        msg_type_info = struct.pack('<L', msg_type)

        return (msg_size_info, msg_type_info, msg_as_bytes)

    @staticmethod
    def make_emergency_msg():
        msg = EmergencyMsg_pb2.EmergencyShutdown()
        msg.TimeTag = int(time.time() * 1000)
        msg.emergencyMsg = "System Failure"
        msg.problem = "Something broke"

        return ProtoMsgFactory.pack_msg(msg)

    @staticmethod
    def make_EMS_update_msg():
        msg = EMSUpdate_pb2.EMSUpdate()
        msg.TimeTag = int(time.time() * 1000)
        msg.load = bytes(999)
        msg.LoadValue = 999

        return ProtoMsgFactory.pack_msg(msg)

    @staticmethod
    def make_power_off_msg():
        msg = PowerOffMsg_pb2.PowerOff()
        msg.TimeTag = int(time.time() * 1000)
        msg.powerOff = "dummy value"

        return ProtoMsgFactory.pack_msg(msg)

    @staticmethod
    def make_update_request_msg():
        msg = UpdateRequestMsg_pb2.UpdateRequest()
        msg.TimeTag = int(time.time() * 1000)
        msg.request = "dummy value"

        return ProtoMsgFactory.pack_msg(msg)

    @staticmethod
    def make_update_msg():
        msg = UpdateMsg_pb2.Update()
        msg.TimeTag = int(time.time() * 1000)
        msg.current = 999
        msg.voltage = 999
        msg.temperature = 999
        msg.irradiance = 999

        return ProtoMsgFactory.pack_msg(msg)

