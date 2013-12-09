from socketIO_client import SocketIO
import re
import requests
from db import Database
from urlparse import urlparse
from bs4 import BeautifulSoup

ADDRESS = 'chat.meatspac.es'
LINKY = '(https?:\/\/)?((?:\.?[-\w]){1,256})(\.\w{1,10})(?::[0-9]{1,5})?(?:\.?\/(?:[^\s.,?:;!]|[.,?:;!](?!\s|$)){0,2048})?'


   
class LinkGetter(object):

    def __init__(self):
        self.db = Database()
        print "Listening to %s" % ADDRESS

    def listen(self):
        socketIO = SocketIO(ADDRESS, 443, secure=True)
        socketIO.on('message', self.on_message)
        socketIO.wait()


    def is_link_to_music(self, url, response, message):
        netloc = urlparse(url).netloc.lower()
        #Sound cloud links
        if netloc == 'soundcloud.com':
            return True
        #Youtube links in the music category
        if netloc == 'youtube.com':
            soup = BeautifulSoup(response.content)
            category = soup.find('p', {'id' : 'eow-category'}).text.lower()
            return category == 'music'
        return 'musicbot' in message




    def do_the_thing(self, key, message):
        if self.db.link_exists(key):
            return
        groups = re.finditer(LINKY, message)
        for g in groups:
            try:
                response = requests.get(g.group(0))
                if response.status_code == 200:
                    print "Found a link! %s" % message
                    url = g.group(0)
                    is_music = self.is_link_to_music(url, response, message)
                    self.db.insert_link(key, message, url, is_music)
            except Exception as e:
                print e
                print "Bad link"
    def on_message(self, *args):
        try:
            data = args[0]
            message = data['chat']['value']['message']
            key = data['chat']['key']
            self.do_the_thing(key, message)
        except Exception as e:
            print e
            print "never crash because crashing would be bad"

if __name__ == '__main__':
    linker = LinkGetter()
    linker.listen()


