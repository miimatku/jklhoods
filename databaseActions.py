import sqlite3 as sql3
from apscheduler.scheduler import Scheduler		#pip install apscheduler==2.1.2
from datetime import datetime,timedelta
import time
import logging
logging.basicConfig()

LIMIT = 400


def getInstagramCount():
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


def getTweetsCount():
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


#Poistaa vanhimmat tietokannan rivit
def deleteOldestInstagram(week_old_id):
	try:
		con = sql3.connect("instagram.db")
		cur = con.cursor()
		cur.execute("DELETE FROM instagram_posts WHERE id < ?", (week_old_id,) )
		con.commit()
		con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()


def deleteOldestTweets(week_old_id):
	try:
		con = sql3.connect("tweets.db")
		cur = con.cursor()
		
		#tagien poisto
		cur.execute("SELECT tweetID FROM twitter_tweets WHERE id < ?", (week_old_id,) )
		rows = cur.fetchall()
		print rows
		tag_deletion = 'DELETE FROM twitter_tags WHERE tweetID IN (' + ','.join(str(r[0]) for r in rows) + ')'
		cur.execute(tag_deletion)
		#tweettien poisto
		cur.execute("DELETE FROM twitter_tweets WHERE id < ?", (week_old_id,) )
		con.commit()
		con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()


def startScheduler():
	schedule = Scheduler()
	schedule.add_interval_job(doCleanUp, days=1)
	schedule.start()
	print 'Scheduler has started.'
	while True:
		time.sleep(5)


#etsii tietokannasta ensimmaisen rivin, joka on yli viikon vanha
def findInstagramLimit():
	today = datetime.now()
	weekAgo = today - timedelta(days=7)
	month = weekAgo.month
	day = weekAgo.day
	query = '%' + str(day) + '.' + str(month) + '%'

	try:
		con = sql3.connect("instagram.db")
		cur = con.cursor()
		cur.execute("SELECT id,time FROM instagram_posts WHERE time LIKE ? ORDER BY id ASC LIMIT 1", (query,) )
		try:		
			row = cur.fetchone()
			con.close()
			return row[0]
		except:
			print "No 1 week old rows found from instagram database"
			con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()
		return None


def findTwitterLimit():	
	today = datetime.now()
	weekAgo = today - timedelta(days=7)
	month = weekAgo.month
	day = weekAgo.day
	query = '%' + str(day) + '.' + str(month) + '%'
	print query

	try:
		con = sql3.connect("tweets.db")
		cur = con.cursor()
		cur.execute("SELECT id,time FROM twitter_tweets WHERE time LIKE ? ORDER BY id ASC LIMIT 1", (query,) )
		try:		
			row = cur.fetchone()
			con.close()
			return row[0]
		except:
			print "No 1 week old rows found from twitter database"
			con.close()
	except Exception, e:
		print "Error &s:" % e.args[0]
		con.close()
		return None		
		
		

def doCleanUp():
	count1 = getInstagramCount()
	count2 = getTweetsCount()

	if getInstagramCount() > LIMIT:
		deleteOldestInstagram(findInstagramLimit())
		if getInstagramCount() < count1:
			print "Successfully deleted %d rows from Instagram database" % count1
		
	else:
		print "No deletions were made to instagram database"
	if getTweetsCount() > LIMIT:
		deleteOldestTweets(findTwitterLimit())
		if getTweetsCount() < count2:
			print "Successfully deleted %d rows from Twitter database" % count2
	else:
		print "No deletions were made to twitter database"

startScheduler()



