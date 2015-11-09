import sqlite3 as lite
import sys
import oembedInstagram

def instagramPosts():
	con = None

	try:
		con = lite.connect('instagram.db')

		data = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts')
		rows = cur.fetchall()
		for row in rows:
			data.append(oembedInstagram.getOEmbed(row[3])])
		return data
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()


def fetchLatest():
	return