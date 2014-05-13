from datetime import datetime

import zmq, json, os, hashlib

context = zmq.Context()

bartok = context.socket(zmq.REQ)
bartok.connect('tcp://localhost:6000')
bartok.send('com.jessebmiller.Model')
inbound_addr, outbound_addr = tuple(bartok.recv().split(';'))

inbox = context.socket(zmq.PULL)
outbound = context.socket(zmq.PUSH)
inbox.connect(inbound_addr)
outbound.bind(outbound_addr)

__content__ = {'404': {'text': '404: This page intentionally left blank'}}

def update_content(_):

    global __content__
    __content__ = {'404': {'text': '404: This page intentionally left blank'}}

    os.system('git clone https://github.com/jessebmiller/writing.git')
    os.system('cd writing && git pull')

    def injest_thought(arg, dirname, names):
        for name in names:
            time = datetime.fromtimestamp(int(name))
            with open("{}/{}".format(dirname, name), 'r') as t:
                text = t.read()
            sha256 = "sha256-{}".format(hashlib.sha256(text).hexdigest())
            __content__[sha256] = { 'time': time.ctime(),
                                    'thought': text}

    def injest_article(arg, dirname, names):
        for name in names:
            with open("{}/{}".format(dirname, name), 'r') as a:
                md = a.read()
            sha256 = "sha256-{}".format(hashlib.sha256(md).hexdigest())
            __content__[sha256] = {'article': md}

    os.path.walk('writing/thoughts', injest_thought, None)
    os.path.walk('writing/articles', injest_article, None)

update_content(None)

handlers = {
    'includes': lambda p: lambda _: [c
                                     for c
                                     in __content__.values()
                                     if c.get(p, False)],
    'recent': lambda n: lambda xs: xs[:int(n)],
    'just': lambda i: lambda _: __content__[i],
    'all': lambda _: lambda _: [c for c in __content__.values()
                                if c.get('text', [])[:4] != '404:'],
    'update_content': lambda _: update_content,
    }

def handle_step(result, step):
    handler, arg = tuple(step.split(' '))
    return handlers[handler](arg)(result)

while True:
    message = inbox.recv()
    request = json.loads(message)
    steps = request['body'].split(';')
    content = reduce(handle_step, steps, None)
    outbound.send(json.dumps({'request': request['request'],
                              'body': content}))
