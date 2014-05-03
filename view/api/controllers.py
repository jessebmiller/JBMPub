import json

from werkzeug.wrappers import Response

# { <type>: <template> }
views_collection = {
    'Text': '<p>{}</p>',
    'Name': '<p class="h-card">{}</p>',
    'Thought': '<div class="thought">{}</div>',
    'Author': '<span class="author">{}</span>',
    'Collection': '<span class="collection">{}</span>',
    'Page': """<!DOCTYPE html>
<html>
  <head>
     <title>Jesse B Miller</title>
  </head>
  <body>
    <style>
      html {{
          font-size: 18px;
      }}
      .content {{
          width: 38%;
          margin: 2em auto;
      }}
    </style>
    <header>
      <div class="content">
        <h1>Jesse B Miller</h1>
      </div>
    </header>
    <div clas="page">
      <div class="content">
        {}
      </div>
    </div>
    <footer>
      <div class="content">
        <h5>Built with JBMPub</h5>
      </div>
    </footer>
  </body>
</html>
"""
    }

def render(obj):

    if not isinstance(obj, dict):
        raise NameError('viewables must be { <type>: list|str|dict|viewable }')

    for k, v in obj.items():
        if isinstance(v, unicode):
            return views_collection[k].format(v)
        elif isinstance(v, dict):
            return render({k: [dict([i]) for i in v.items()]})
        elif isinstance(v, list):
            return views_collection[k].format(''.join(map(render, v)))
        else:
            raise NameError('viewable values must be one of (list, str, dict)')
    return ''

def root(req):

    def get(req):
        return "views service, POST some viewable content"

    def post(req):
        content = json.loads(req.values['viewable'])
        return render(content)

    if req.method == 'GET':
        return Response(get(req))
    elif req.method == 'POST':
        return Response(post(req))
    return ("could not handle root request")

def views(req, type_=None):

    def get(req):
        if type_ is not None:
            return views_collection[type_]
        else:
            return json.dumps(
                map(lambda x: dict([x]),
                    views_collection.items()
                    )
                )

    def post(req):
        if type_ is not None:
            template = req.values['template']
            views_collection[type_] = template
        else:
            return "usage: POST /v0/views/<type> ... "

    if req.method == 'GET':
        return Response(get(req))
    elif req.method == 'POST':
        return Response(post(req))
    return ("could not handle root request")
