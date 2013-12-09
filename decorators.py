import json
from flask import Flask, g, Response, render_template, request




#Yea i put the paginator before the view method...not correct all the time. 
#
#sup
def paginate(predicate = 'music >= 0', num_links = 20):
    def __page(fn):
        def wrapped(*args, **kwargs):
            offset = int(request.args.get('offset', 0))
            link_count = g.db.link_count(predicate)
            next = None
            prev = None
            if num_links + offset < link_count:
                next = offset + num_links
            if offset > 0:
                prev = offset - num_links

            return fn(offset, next, prev, link_count)
        return wrapped
    return __page


def json_view(fn):
    def wrapped(*args, **kwargs):
        r, status = fn(*args, **kwargs)
        return Response(response=json.dumps(r), status=status, headers=None, mimetype='application/json', content_type=None)
    return wrapped


