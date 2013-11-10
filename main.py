from flask import Flask
from flask import g, render_template, request
import listener
from db import Database
from threading import Thread
import re
app = Flask(__name__)

NUM_LINKS = 20



@app.route("/")
def links():
    offset = int(request.args.get('offset', 0))
    print "Getting from %s" % offset
    links = g.db.get_links(offset = offset, limit = NUM_LINKS)
    link_count = g.db.link_count()


    next = None
    prev = None
    if len(links) + offset < link_count:
        next = offset + NUM_LINKS
    if offset > 0:
        prev = offset - NUM_LINKS

    return render_template('links.html', links = links, next = next, prev = prev)



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

