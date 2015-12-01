import sqlite3 as lite
import sys
from flask import jsonify


def instagramPosts():
	con = None
	try:
		con = lite.connect('instagram.db')

		data = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts ORDER BY id DESC LIMIT 10')
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
			
def fetchInstagram(shortcode):
	con = None
	try:
		con = lite.connect('instagram.db')
		posts = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts WHERE id > (SELECT id FROM instagram_posts WHERE shortcode LIKE  ?)', (shortcode,))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		return jsonify(result=posts)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()


def fetchWithTag(tag):
	try:
		con = lite.connect('instagram.db')
		data = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts,instagram_tags WHERE instagram_posts.mediaID=instagram_tags.mediaID AND hashtag LIKE ? LIMIT 10', (tag,) )
		rows = cur.fetchall()
	except Exception, e:
		print "Error &s:" % e.args[0]
	return
	
def fetchNext(shortcode):
	con = None
	try:
		con = lite.connect('instagram.db')
		posts = []
		cur = con.cursor()
		cur.execute('SELECT shortcode FROM instagram_posts WHERE id < (SELECT id FROM instagram_posts WHERE shortcode LIKE  ?) LIMIT 10', (shortcode,))
		rows = cur.fetchall()
		for row in rows:
			posts.append([str(row[0])])
		return jsonify(result=posts)
	except lite.Error, e:
		print "Error &s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()
