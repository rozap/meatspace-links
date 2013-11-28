import sqlite3




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

    def get_links(self, offset = 0, limit = 5):
        cur = self._db.cursor()
        cur.execute(''' SELECT key, message, link, created FROM links ORDER BY created DESC LIMIT ? OFFSET ?''', (limit, offset))
        return cur.fetchall()

    def link_count(self):
        cur = self._db.cursor()
        cur.execute(''' SELECT count(*) AS c FROM links''')
        return cur.fetchone()['c']



    def insert_link(self, key, message, link):
        print "Insert %s and %s @ %s" % (key, message, link)
        cur = self._db.cursor()
        cur.execute(''' INSERT OR REPLACE INTO
                            links(message, link, key) 
                        VALUES(?, ?, 
                                COALESCE((SELECT key FROM links WHERE key = ?), ?)
                            ) ''', (message, link, key, key))
        self._db.commit()

    def insert_link_dt(self, key, message, link, dt):
        print "Insert %s and %s @ %s" % (key, message, link)
        cur = self._db.cursor()
        cur.execute(''' INSERT OR REPLACE INTO
                            links(message, link, key, created) 
                        VALUES(?, ?, ?,
                                COALESCE((SELECT key FROM links WHERE key = ?), ?)
                            ) ''', (message, link, dt, key, key))
        self._db.commit()


    def build(self):
        self._db.execute('''CREATE TABLE links (key text, message text, link text, created timestamp DEFAULT CURRENT_TIMESTAMP)''')