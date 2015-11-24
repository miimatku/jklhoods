#!/usr/bin/python
from flask import Flask,request, Response,redirect,url_for
from instagram import client, subscriptions
from twisted.internet import reactor
import json
import sys, logging
import time
#import threading
import multiprocessing
import sqlite3 as sql3
from datetime import datetime

CLIENT_ID='efe6cccbd3ac4e75b842c957e954c569'
CLIENT_SECRET='bdadba8a4b274b45bdfcb306cfd6b120'
ACCESS_TOKEN='1442727277.5b9e1e6.71468fed77d14c4fb1d3a41b2644d4de'
COUNT = 1
CALLBACK_HEROKU = 'https://shielded-wave-4959.herokuapp.com/callback'
CALLBACK_LOCAL = 'http://localhost:5000/oauth_callback'
CALLBACK_TUNNEL = 'https://nzmpqlpmhe.localtunnel.me/realtime' #lt --port 8000 --subdomain nzmpqlpmhe

tag = 'swag'
subID = 0

reactor = None
"""
TODO
subscription poistaminen suljettaessa ohjelma
tietokantaan tallennus
multiprocessingin aiheuttamat virheet pois

"""


con = sql3.connect("instagram.db")

cur = con.cursor()

app = Flask(__name__)

def subscribeToTag(topic):
   r = api.create_subscription(object = 'tag',
                            object_id = topic,
                            aspect = 'media',
                            callback_url = CALLBACK_TUNNEL,
                            client_id = CLIENT_ID,
                            client_secret = CLIENT_SECRET)
   global subID
   subID = r['data']['id']
							
    
@app.route('/', methods=['GET','POST'])
def index():
   return 'jotain'

#hakee uuden paivityksen ID:n
def fetchNewUpdate(amount=1):
  global tag
  tagged_media, next_ = api.tag_recent_media(tag_name=tag, count=amount)
  for media in tagged_media:
     #id = media.id
     comment = media.caption
     print comment
     user = media.user.username
     userID = media.user.id
     timestamp = media.created_time
     media_link = media.link #linkki paivitykseen
     shortcode = media_link.split("/")[4]
	 
     savetoDataBase(userID,user,timestamp,shortcode)
  return True


def savetoDataBase(userID,user,timestamp,shortcode):
  """
   print str(userID) + "#" + str(user) + "#" + str(shortcode) + str(timestamp.strftime("%d.%m.%Y %H:%M"))
   try:
     cur.execute("INSERT INTO instagram_posts (id, username, time, shortcode) VALUES (?, ?, ?, ?)",
     (str(userID), str(user), timestamp.strftime("%d.%m.%Y %H:%M"), str(shortcode)))
     con.commit()
   except sql3.Error, e:
     print "Error &s:" % e.args[0]
     """
   return 


#reactor versio
@app.route('/realtime', methods=['POST','GET'])
def callback(): 
   global reactor
   if request.method == 'GET':
      mode         = request.values.get('hub.mode')
      challenge    = request.values.get('hub.challenge')
      verify_token = request.values.get('hub.verify_token')
      if challenge:
         return Response(challenge)
   else:
       x_hub_signature = request.headers.get('X-Hub-Signature')
       raw_response    = request.data
       if raw_response:
          fetchNewUpdate()
       try:
           reactor.process(CLIENT_SECRET, raw_response, x_hub_signature)
       except subscriptions.SubscriptionVerifyError:
           logging.error('Instagram signature mismatch')
   return Response("") #ei tarvitse vastausta.

api = client.InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token= ACCESS_TOKEN) 

#tekee subscription-toiminnon 5 sekunnin kuluttua flask-sovelluksen kaynnistyttya
def doSubscribe():
    print "Subscription process starting"
    time.sleep(3)
    global tag
    subscribeToTag(tag)
    print 'Subscription process ended'
	
def startApp():
    global app
    app.run(debug=True, port=8000, use_reloader=True)


def stop_subscription():
  api.delete_subscriptions(id=subID)


reactor = subscriptions.SubscriptionsReactor()


class ApplicationProcess(multiprocessing.Process):

    def __init__(self, ):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()

    def run(self):
        try:
            startApp()
        except (KeyboardInterrupt, SystemExit):
            print "Exiting..."

    def terminate(self):
        print "Flask application shutdown initiated"
        self.exit.set()

class SubscriptionProcess(multiprocessing.Process):

    def __init__(self, ):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()

    def run(self):
        try:
          doSubscribe()
        except Exception, e:
          print "Error during subscription process"
          print e

    def terminate(self):
        self.exit.set()


if __name__ == '__main__':
   """ ###Threading###

   appProcess = threading.Thread(target=startApp)
   appProcess.daemon = True
   appProcess.start()
   subProcess = threading.Thread(target=doSubscribe)
   subProcess.daemon = False
   subProcess.start()

   """

   flaskapp = ApplicationProcess()
   flaskapp.start()
   subProcess = SubscriptionProcess()
   subProcess.start()

   while True:
      try:
        time.sleep(1)
      except KeyboardInterrupt, SystemExit:
        print "Exiting..."
        sys.exit(0)
