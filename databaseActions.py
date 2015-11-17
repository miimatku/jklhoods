import sqlite3 as sql3

def getinstagramCount():
	row = None
	try:
		con = sql3.connect("instagram.db")
		cur = con.cursor()
		cur.execute("SELECT COUNT(*) as count FROM instagram_posts")
		row = cur.fetchone()
		con.close()
	except Exception, e:
		con.close()
	return row


def getTwitterCount():
	row = None
	try:
		con = sql3.connect("tweets.db")
		cur = con.cursor()
		cur.execute("SELECT COUNT(*) as count FROM twitter_tweets")
		row = cur.fetchone()
		con.close()
	except Exception, e:
		con.close()
	return row

def getTagsCount():
	row = None
	try:
		con = sql3.connect("tweets.db")
		cur = con.cursor()
		cur.execute("SELECT COUNT(*) as count FROM twitter_tags")
		row = cur.fetchone()
		con.close()
	except Exception, e:
		con.close()
	return row


def deleteOldestInstagram(amount):
	try:
		con = sql3.connect("instagram.db")
		cur = con.cursor()
		cur.execute("DELETE FROM instagram_posts WHERE id IN (SELECT id FROM instagram_posts ORDER BY id ASC LIMIT ?)", (amount,) )
		con.commit()
		con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()


def deleteOldestTweets(amount):
	try:
		con = sql3.connect("tweets.db")
		cur = con.cursor()
		
		#tagien poisto
		cur.execute("SELECT tweetID FROM twitter_tweets ORDER BY id ASC LIMIT ?", (amount,) )
		rows = cur.fetchall()
		tag_deletion = 'DELETE FROM twitter_tags WHERE tweetID IN (' + ','.join(str(r[0]) for r in rows) + ')'
		cur.execute(tag_deletion)
		
		#tweettien poisto
		cur.execute("DELETE FROM twitter_tweets WHERE id IN (SELECT id FROM twitter_tweets ORDER BY id ASC LIMIT ?)", (amount,) )
		
		con.commit()
		con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()
