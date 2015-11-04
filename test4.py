#!/usr/bin/python
from flask import Flask,request, Response,redirect,url_for
from instagram import client, subscriptions
from twisted.internet import reactor
import json
import sys, logging
import time
from multiprocessing import Process
import oembedInstagram
import atexit

CLIENT_ID='efe6cccbd3ac4e75b842c957e954c569'
CLIENT_SECRET='bdadba8a4b274b45bdfcb306cfd6b120'
ACCESS_TOKEN='1442727277.5b9e1e6.71468fed77d14c4fb1d3a41b2644d4de'
COUNT = 1
CALLBACK_HEROKU = 'https://shielded-wave-4959.herokuapp.com/callback'
CALLBACK_LOCAL = 'http://localhost:5000/oauth_callback'
CALLBACK_TUNNEL = 'https://nzmpqlpmhe.localtunnel.me/realtime' #lt --port 8000 --subdomain nzmpqlpmhe

f1=open('./testfile.txt', 'a')
tag = 'swag'
subID = 0

idListing = []
test = ''
lista = []
reactor = None

"""
TODO
susbcription poistaminen suljettaessa ohjelma
tietokantaan tallennus
multiprocessingin aiheuttamat virheet pois



"""


app = Flask(__name__)

def subscribeToTag(topic):
   print CLIENT_SECRET
   r = api.create_subscription(object = 'tag',
                            object_id = topic,
                            aspect = 'media',
                            callback_url = CALLBACK_TUNNEL,
                            client_id = CLIENT_ID,
                            client_secret = CLIENT_SECRET)
   global subID
   subID = r['data']['id']
							
   
def parse_update(update):
   #instagram_userid = update['object_id']
   #id =  str(instagram_userid)
   lista.append('asda')
   return redirect(url_for('showInstagram'))
   
def getImageURLs():
   popular_media = api.media_popular(count=COUNT)
   return popular_media


@app.route('/showInstagram')
def showInstagram():
   #stop_subscription()
   global idListing
   return str(idListing)
   

@app.route('/', methods=['GET','POST'])
def index():
   lista = getImageURLs()
   #str-funktiolla toimii
   #global sub
   return str(lista[0])


#hakee uuden paivityksen ID:n
def fetchNewUpdate(amount=1):
  global tag
  global idListing
  tagged_media, next_ = api.tag_recent_media(tag_name=tag, count=amount)
  for media in tagged_media:
     id = media.id
     #user = media.user
     #timestamp = media.created_time
     media_link = media.link #linkki paivitykseen
     shortcode = media_link.split("/")[4]
     #alla oleva funktio jarkea tehda myohemmin?
     embed = oembedInstagram.getOEmbed(shortcode)
     #savetoDataBase()
     idListing.append("a")
  return idListing


def savetoDataBase():
   #TODO
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
       print raw_response

       try:
           reactor.process(CLIENT_SECRET, raw_response, x_hub_signature)
       except subscriptions.SubscriptionVerifyError:
           logging.error('Instagram signature mismatch')
   return Response("") #ei tarvitse vastausta.

api = client.InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token= ACCESS_TOKEN) 

#tekee subscription-toiminnon n. 5 sekunnin kuluttua flask-sovelluksen kaynnistyttya
def doSubscribe():
    print "Subscription process starting"
    time.sleep(5)
    global tag
    subscribeToTag(tag)
    print 'Subscription process ended'
	
def startApp():
    global app
    app.run(debug=True, port=8000)


def stop_subscription():
  api.delete_subscriptions(id=subID)


reactor = subscriptions.SubscriptionsReactor()
#atexit.register(stop_subscription) #funktio, joka suoritetaan ohjelman sulkeutuessa

def main():
   server = Process(target=startApp)
   server.start()
   sub = Process(target=doSubscribe)
   sub.start()

if __name__ == '__main__':
   try:
        main()
   except KeyboardInterrupt:
        raise

