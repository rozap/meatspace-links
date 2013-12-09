
from db import Database
from listener import LinkGetter


def main():
	d = Database()
	g = LinkGetter()

	links = d.get_links(limit = 100000)

	cur = d._db.cursor()
	cur.execute("DELETE FROM links")
	d._db.commit()

	for l in links:
		print l
		g.do_the_thing(l['key'], l['message'])

if __name__ == '__main__':
	main()