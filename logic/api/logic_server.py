import zmq, json

context = zmq.Context()
bartok = context.socket(zmq.REQ)
bartok.connect('tcp://localhost:6000')
bartok.send('com.jessebmiller.Logic')
inbound_addr, outbound_addr = tuple(bartok.recv().split(';'))

inbox = context.socket(zmq.PULL)
outbound = context.socket(zmq.PUSH)
inbox.connect(inbound_addr)
outbound.bind(outbound_addr)

collections = {
    'thoughts': 'thought',
    'articles': 'article',
    }

while True:
    path = inbox.recv()
    if path == '/':
        query = 'all things;recent 10'
    elif path.split('-')[0] == '/sha256':
        query = "just {}".format(path.split('/')[1])
    elif collections.get(path.split('/')[1], False):
        query = "includes {};recent 10".format(collections[path.split('/')[1]])
    else:
        query = "just 404"

    request = json.dumps({'request': {'path': path},
                          'body': query})
    outbound.send(request)
