from werkzeug.wrappers import Request
from werkzeug.routing import Map, Rule, RequestRedirect, NotFound

from controllers import home, content

url_map = Map([
        Rule('/v0/', endpoint=home),
        Rule('/v0/<collection>/', endpoint=content),
        Rule('/v0/<collection>/<key>', endpoint=content),
        ])

def handle_request(req, url_map):
    endpoint, args = url_map.bind_to_environ(req.environ).match()
    return endpoint(req, **args)

@Request.application
def app(req):
    try:
        return handle_request(req, url_map)
    except KeyError, e:
        return NotFound("could not find {}".format(e))


if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 4000, app, use_reloader=True, use_debugger=True)
