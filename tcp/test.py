import os

from tcp_client import TCPClient


address = ('localhost', 10000)


kidpid = os.fork()

if kidpid == 0:
    c1 = TCPClient(address)
    c1.post()
else:
    c2 = TCPClient(address)
    c2.post() 






