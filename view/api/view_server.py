import zmq, json

from markdown import markdown

from collections import namedtuple
from hashlib import sha256

context = zmq.Context()

bartok = context.socket(zmq.REQ)
bartok.connect('tcp://localhost:6000')
bartok.send('com.jessebmiller.View')
inbound_addr, outbound_addr = tuple(bartok.recv().split(';'))

inbox = context.socket(zmq.PULL)
outbound = context.socket(zmq.PUSH)
inbox.connect(inbound_addr)
outbound.bind(outbound_addr)

Page = namedtuple('Page', 'style page')

with open('page.html.fmt', 'r') as pagefmt:
    pagefmt = pagefmt.read()

def _thought(string):
    href = "/sha256-{}".format(sha256(string).hexdigest())
    return "<a href='{}'><p class='thought'>{}</p></a>".format(href, string)

def _article(md):
    href = "/sha256-{}".format(sha256(md).hexdigest())
    lines = markdown(md).split('\n')
    lines[0] = "<a href={}>{}</a>".format(href, lines[0])
    return '\n'.join(lines);

types = {
    'thought': _thought,
    'article': _article,
    'text': lambda t: t,
    'time': lambda t: "<time>{}</time>".format(t),
}

def render(content):
    if isinstance(content, Page):
        return pagefmt.format(style=content.style, page=render(content.page))
    if isinstance(content, unicode):
        return content
    if isinstance(content, dict):
        piece = '\n'.join(map(lambda x: types[x](render(content[x])),
                              content.keys()))
        return "<div class='piece'>{}</div>".format(piece)
    if isinstance(content, list):
        return "<span class='collection'>{}</span>".format(
            '\n<span class="collectionDevider"></span>'.join(
                map(render, content)))

    return "unknown type {}".format(content)

while True:
    message = inbox.recv()
    request = json.loads(message)
    style = '/static/style.css'
    outbound.send(render(Page(style, request['body'])))
