from flask import Flask, g, render_template, request
import listener
from db import Database
from decorators import json_view, paginate
from threading import Thread
import re
import random
app = Flask(__name__)

NUM_LINKS = 20


@app.route("/", endpoint = 'index')
@paginate(num_links = NUM_LINKS)
def links(offset, next, prev, link_count):
    links = g.db.get_links(offset = offset, limit = NUM_LINKS)
    return render_template('links.html', links = links, next = next, prev = prev)



#Endpoint to return a JSON list of music
@app.route("/api/music", endpoint = 'music')
@paginate(predicate = 'music = 1', num_links = NUM_LINKS)
@json_view
def music(offset, next, prev, link_count):
    links = g.db.get_music(offset = offset, limit = NUM_LINKS)
    response = {
        'meta' : {
            'link_count' : link_count
        },
        'music' : links
    }
    if next:
        response['meta']['next'] = '%s?offset=%s' % (request.url_rule, next)
    if prev:
        response['meta']['previous'] = '%s?offset=%s' % (request.url_rule, prev)

    return response, 200

@app.route("/api/music/random", endpoint = 'music/random')
@paginate(predicate = 'music = 1', num_links = NUM_LINKS)
@json_view
def music(offset, next, prev, link_count):
    some_number = random.randint(0, link_count-1)
    link = g.db.get_music(offset = some_number, limit = 1)[0]
    return link, 200






@app.before_request
def before_request():
    g.db = Database()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close() 



if __name__ == "__main__":
    app.run(debug = True)

