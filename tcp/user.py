"""Demo user for tcp_client.py"""

from tcp_client import TCPClient
from proto_msg_factory import ProtoMsgFactory

def print_this(dic):
    for item in dic:
        print(item)

""" msg = ProtoMsgFactory.make_emergency_msg()
print(msg) """

server_address = 'localhost'
port = 10000

user = TCPClient(server_address, port)
print(user.post("foo"))

ems_update_message = ProtoMsgFactory.make_EMS_update_msg()

print_this(ems_update_message)

power_off_msg = ProtoMsgFactory.make_power_off_msg()
print_this(power_off_msg)

update_request_msg = ProtoMsgFactory.make_update_request_msg()
print_this(update_request_msg)

update_msg = ProtoMsgFactory.make_update_msg()
print_this(update_msg)


