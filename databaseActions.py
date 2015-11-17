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


def gettwitterCount():
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


def deleteOldestInstagram(amount):
	try:
		con = sql3.connect("instagram.db")
		cur = con.cursor()
		cur.execute("DELETE FROM instagram_posts WHERE id IN (SELECT id FROM instagram_posts ORDER BY id ASC LIMIT ?)"(amount,) )
		con.close()
	except Exception, e:
		con.close()


def deleteOldestTweets(amount):
	try:
		con = sql3.connect("tweets.db")
		cur = con.cursor()
		#cur.execute("DELETE FROM twitter_tweets WHERE id IN (SELECT id FROM twitter_tweets ORDER BY id ASC LIMIT ?)"(amount,) )
		#cur.execute(("""DELETE twitter_tweets, twitter_tags  FROM twitter_tweets ORDER BY id ASC LIMIT 1 INNER JOIN twitter_tags WHERE 
		#	twitter_tweets.tweetID = twitter_tags.tweetID"""))

		cur.execute("""DELETE tweets.*, tags.*  
			            FROM twitter_tweets as tweets
			            LEFT JOIN twitter_tags as tags ON tweets.tweetID = tags.tweetID
			            ORDER BY id ASC LIMIT 1
					""")

		con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()






deleteOldestTweets(1)


print gettwitterCount()
print getinstagramCount()
