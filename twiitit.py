import sqlite3 as lite
import sys

def twiits():
	con = None

	try:
		con = lite.connect('tweets.db')

		tweets = []
		cur = con.cursor()
		cur.execute('SELECT tweetID FROM twitter_tweets LIMIT 10')
		#filterointia varten
		#cur.execute('SELECT tweet.id FROM twitter_tweets tweet INNER JOIN twitter_tags tag ON tweet.id = tag.id')
		rows = cur.fetchall()
		for row in rows:
			tweets.append([row[0]])
		return tweets
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()