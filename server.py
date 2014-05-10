import zmq, re

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule, RequestRedirect, NotFound

context = zmq.Context()
bartok = context.socket(zmq.REQ)
bartok.connect('tcp://localhost:6000')
bartok.send('com.jessebmiller.Proxy')
inbound_addr, outbound_addr = tuple(bartok.recv().split(';'))

inbox = context.socket(zmq.PULL)
outbound = context.socket(zmq.PUSH)
inbox.connect(inbound_addr)
outbound.bind(outbound_addr)

def dispatch(req):

    path = req.path

    if re.match('^/static/', path):
        with open(path[1:], 'r') as staticfile:
            return Response(staticfile.read(), content_type='text/css')
    else:
        outbound.send(str(req.path))
        response = inbox.recv()
        return Response(response, content_type='text/html')

@Request.application
def app(req):
    try:
        return dispatch(req)
    except Exception, e:
        return NotFound(e)


if __name__ == "__main__":
    import sys
    from werkzeug.serving import run_simple
    run_simple(sys.argv[1], 4000,
               app,
               use_reloader=False,
               use_debugger=True,
               threaded=True
               )
