import sys

from werkzeug.wrappers import Request
from werkzeug.routing import Map, Rule, RequestRedirect, NotFound

from controllers import root, views

url_map = Map([
        Rule('/v0/', endpoint=root),
        Rule('/v0/views/', endpoint=views),
        Rule('/v0/views/<type_>', endpoint=views)
        ])

def handle_request(req, url_map):
    endpoint, args = url_map.bind_to_environ(req.environ).match()
    return endpoint(req, **args)

@Request.application
def app(req):
    return handle_request(req, url_map)


if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple(sys.argv[1], 4001, app, use_reloader=True, use_debugger=True)
