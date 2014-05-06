from collections import defaultdict

import zmq

context = zmq.Context()
server_socket = context.socket(zmq.REP)
server_socket.bind('tcp://*:6000')

class NewAddr(object):

    def __init__(self, first_addr):
        self.last_addr = first_addr

    def __call__(self):
        self.last_addr += 1
        return self.last_addr

new_address = NewAddr(6000)

inbound_addresses = defaultdict(new_address)

outbound_targets = {
    'com.jessebmiller.Proxy': 'com.jessebmiller.Logic',
    'com.jessebmiller.Logic': 'com.jessebmiller.Model',
    'com.jessebmiller.Model': 'com.jessebmiller.View',
    'com.jessebmiller.View': 'com.jessebmiller.Proxy',
    }

def inbound(socket_name):
    return "tcp://localhost:{}".format(
        inbound_addresses[socket_name])

def outbound(socket_name):
    return "tcp://*:{}".format(
        inbound_addresses[outbound_targets[socket_name]])

while True:
    request = server_socket.recv()
    print 'bartok got', request
    in_addr = inbound(request)
    print '  > in', in_addr
    out_addr = outbound(request)
    print '  > out', out_addr
    server_socket.send(b';'.join([in_addr, out_addr]))
