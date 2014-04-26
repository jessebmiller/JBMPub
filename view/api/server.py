"""
Views API

given a context and viewable json, return a representation of the data

example:
POST /html HTTP/1.1
...

{"Text":"some text to render"}

would respond with the body

<p>some text to render</p>

if a template of <p>{{Text}}</p> were registered for html:text

"""

from flask import Flask

registry = {
    'Text': '<p>{{Text}}</p>',
    'Time': '<span class="time">{{ Time }}</span>'
    'Author': '<div class="h-card">{{ children this }}</div>'
    'Thought': '<div class="thought">{{ children this }}</div>'
}

@app.context_processor
def utility_processor():
    def children(obj):
        rendered = []
        for k in obj:
            rendered.append(render(obj[k]))
        return u''.join(rendered)
    return dict(children=children)

app = Flask(__name__)

@app.route('/html/')
