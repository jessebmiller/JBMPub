import json
from urllib2 import urlopen

from werkzeug.wrappers import Response

model_endpoint = 'http://localhost:4000'
view_endpoint = 'http://localhost:4001'

def root(req):
    return Response('temp root response')

def content(req, collection, hash_=None):
    """ the hashed item in the collection, or the collection itself """
    content_request = "{}/v0/{}/".format(model_endpoint, collection)
    if hash_:
        content_request += hash_
    content = json.loads(urlopen(content_request).read())
    if not hash_:
        content = {'Collection': content}
    content = {"Page": content}
    viewable = "viewable={}".format(json.dumps(content))
    view_request = "{}/v0/".format(view_endpoint)
    html = urlopen(view_request, viewable).read()
    return Response(html, mimetype='text/html')
