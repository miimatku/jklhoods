import sqlite3 as lite
import sys

def instagramPosts():
	con = None

	try:
		con = lite.connect('instagram.db')

		data = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts LIMIT 10')
		rows = cur.fetchall()
		for row in rows:
			if row:
				data.append(row[0])
			else:
				continue
		return data
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()


def fetchLatest():
	return