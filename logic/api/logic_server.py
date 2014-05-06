import zmq

context = zmq.Context()
bartok = context.socket(zmq.REQ)
bartok.connect('tcp://localhost:6000')
bartok.send('com.jessebmiller.Logic')
inbound_addr, outbound_addr = tuple(bartok.recv().split(';'))

inbox = context.socket(zmq.PULL)
outbound = context.socket(zmq.PUSH)
inbox.connect(inbound_addr)
outbound.bind(outbound_addr)

while True:
    path = inbox.recv()
    print "Logic got {}".format(path)
    outbound.send('logic $ {}'.format(path))
