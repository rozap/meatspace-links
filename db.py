import sqlite3


def read(fn):
    def wrapped(self, *args, **kwargs):
        cursor = self._db.cursor()
        return fn(self, cursor, *args, **kwargs)
    return wrapped


def write(fn):
    def wrapped(self, *args, **kwargs):
        cursor = self._db.cursor()
        res = fn(self, cursor, *args, **kwargs)
        self._db.commit()
        return res
    return wrapped


class Database(object):
    _db = None

    def __init__(self, *args, **kwargs):
        self._db = sqlite3.connect('linky.db', isolation_level = None)
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self._db.row_factory = dict_factory


    def close(self):
        self._db.close()

    @read
    def link_exists(self, cursor,  key):
        cursor.execute(''' SELECT count(*) AS c FROM links WHERE key = ? ''', (key, ))
        return not cursor.fetchone()['c'] == 0

    @read
    def get_links(self, cursor, offset = 0, limit = 20):
        cursor.execute('''
                            SELECT key, message, link, created 
                            FROM links
                            ORDER BY created DESC 
                            LIMIT ? OFFSET ?''', 
                    (limit, offset)
                )
        return cursor.fetchall()

    @read
    def link_count(self, cursor, predicate = 'music >= 0'):
        cursor.execute('SELECT count(*) AS c FROM links WHERE %s' % predicate)
        return cursor.fetchone()['c']


    @read
    def get_music(self, cursor, offset = 0, limit = 5):
        cursor.execute('''
                            SELECT key, message, link, created 
                            FROM links
                            WHERE music = 1
                            ORDER BY created DESC 
                            LIMIT ? OFFSET ?''', 
                    (limit, offset)
                )
        return cursor.fetchall()

    @write
    def insert_link(self, cursor,  key, message, link, is_music):
        music = 0
        if is_music:
            music = 1
        cursor.execute(''' INSERT OR REPLACE INTO
                            links(message, link, key, music) 
                        VALUES(?, ?, ?, ?) ''', (message, link, key, music))



    def build(self):
        self._db.execute('''CREATE TABLE links (key text, message text, link text, created timestamp DEFAULT CURRENT_TIMESTAMP, music integer DEFAULT 0)''')
