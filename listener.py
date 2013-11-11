from socketIO_client import SocketIO
import re
import requests
from db import Database

ADDRESS = 'chat.meatspac.es'
LINKY = '(https?:\/\/)?((?:\.?[-\w]){1,256})(\.\w{1,10})(?::[0-9]{1,5})?(?:\.?\/(?:[^\s.,?:;!]|[.,?:;!](?!\s|$)){0,2048})?'


   
class LinkGetter(object):

    def __init__(self):
        self.db = Database()
        print "Listening to %s" % ADDRESS
        socketIO = SocketIO(ADDRESS, 443, secure=True)
        socketIO.on('message', self.on_message)
        socketIO.wait()



    def do_the_thing(self, key, message):
        groups = re.finditer(LINKY, message)
        for g in groups:
            try:
                response = requests.get(g.group(0))
                if response.status_code == 200:
                    print "Found a link! %s" % message
                    self.db.insert_link(key, message, g.group(0))
            except:
                print "Bad link"
    def on_message(self, *args):
        try:
            data = args[0]
            message = data['chat']['value']['message']
            key = data['chat']['key']
            print message
            self.do_the_thing(key, message)
        except:
            print "never crash because crashing would be bad"

if __name__ == '__main__':
    linker = LinkGetter()


