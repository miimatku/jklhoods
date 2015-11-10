#!/usr/bin/python
from flask import Flask,request, Response,redirect,url_for
from instagram import client, subscriptions
from twisted.internet import reactor
import json
import sys, logging
import time
import multiprocessing
import sqlite3 as sql3
from datetime import datetime

"""
https://api.instagram.com/v1/subscriptions?client_secret
=bdadba8a4b274b45bdfcb306cfd6b120&client_id=efe6cccbd3ac4e75b842c957e954c569
"""

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
TODO:
subscription poistaminen suljettaessa ohjelma
multiprocessingin aiheuttamat virheet pois

"""

def subscribeToTag(topic):
   r = api.create_subscription(object = 'tag',
                            object_id = topic,
                            aspect = 'media',
                            callback_url = CALLBACK_TUNNEL,
                            client_id = CLIENT_ID,
                            client_secret = CLIENT_SECRET)
   global subID
   subID = r['data']['id']
							

#hakee uuden paivityksen ja paivittaa sen tietokantaan
def fetchNewUpdate(amount=1):
  global tag
  tagged_media, next_ = api.tag_recent_media(tag_name=tag, count=amount)
  for media in tagged_media:
     #id = media.id
     user = media.user.username
     userID = media.user.id
     timestamp = media.created_time
     media_link = media.link #linkki paivitykseen
     shortcode = media_link.split("/")[4]
	 
     savetoDataBase(userID,user,timestamp,shortcode)
  return True


def savetoDataBase(userID,user,timestamp,shortcode):
   try:
     con = sql3.connect("instagram.db")
     cur = con.cursor()
     cur.execute("INSERT INTO instagram_posts (id, username, time, shortcode) VALUES (?, ?, ?, ?)",
     (str(userID), str(user), str(timestamp.strftime("%d.%m.%Y %H:%M")), str(shortcode)))
     con.commit()
   except sql3.Error, e:
     print "Error &s:" % e.args[0]
   con.close()
   return 


#reactor versio
def callback(): 
   global reactor
   if request.method == 'GET':
      mode         = request.values.get('hub.mode')
      challenge    = request.values.get('hub.challenge')
      verify_token = request.values.get('hub.verify_token')
      if challenge:
         return Response(challenge)
   else: #POST
       x_hub_signature = request.headers.get('X-Hub-Signature')
       raw_response    = request.data
       if raw_response:
          fetchNewUpdate()
       try:
           reactor.process(CLIENT_SECRET, raw_response, x_hub_signature)
       except subscriptions.SubscriptionVerifyError:
           logging.error('Instagram signature mismatch')
   return Response("") #ei tarvitse vastausta.

#tekee subscription-toiminnon 3 sekunnin kuluttua flask-sovelluksen kaynnistyttya
def doSubscribe():
    print "Subscription process starting"
    time.sleep(3)
    global tag
    subscribeToTag(tag)
    print 'Subscription process ended'


def stop_subscription():
  api.delete_subscriptions(id=subID, client_secret=CLIENT_SECRET)
  
  
def list_subscriptions():
  api.list_subscriptions(callback_url=CALLBACK_TUNNEL)


api = client.InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token= ACCESS_TOKEN) 
reactor = subscriptions.SubscriptionsReactor()


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
   subProcess = SubscriptionProcess()
   subProcess.start()
   
   
def startSubscription():
   #if (list_subscriptions() == None):
      subProcess = SubscriptionProcess()
      subProcess.start()