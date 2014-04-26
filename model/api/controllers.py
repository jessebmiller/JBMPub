import json

from datetime import datetime
from hashlib import sha224 as hash_

from werkzeug.wrappers import Response

timefmt = '%Y-%m-%d_%H:%M:%S.%f'

# content { <collection> { <hash> : <resource>, ...} ... }
collections = {}

def home(req):
    return Response('Temp Root Response')

def content(req, collection, key=None):

    def get(req, key):
        if key is not None:
            return collections[collection][key]
        else:
            return json.dumps([
                collections[collection][k]
                for k
                in collections[collection]
                ])

    def post(req):
        content = json.dumps(json.loads(req.values['content']))
        key = hash_(content).hexdigest()
        if not collections.get(collection, None):
            collections[collection] = {}
        collections[collection][key] = content
        return "going to make this json someday but I stored {} at {}".format(
            content, key)

    if req.method == 'GET':
        return Response(get(req, key))
    elif req.method == 'POST':
        return Response(post(req))

    return Response('could not handle thoughts request')
