#!/usr/bin/python
from flask import Flask,request, Response,redirect,url_for
from instagram import client, subscriptions
from twisted.internet import reactor
import json
import sys, logging
import time
from multiprocessing import Process

CLIENT_ID='efe6cccbd3ac4e75b842c957e954c569'
CLIENT_SECRET='bdadba8a4b274b45bdfcb306cfd6b120'
ACCESS_TOKEN='1442727277.5b9e1e6.71468fed77d14c4fb1d3a41b2644d4de'
COUNT = 1
CALLBACK_HEROKU = 'https://shielded-wave-4959.herokuapp.com/callback'
CALLBACK_LOCAL = 'http://localhost:5000/oauth_callback'
CALLBACK_TUNNEL = 'https://nzmpqlpmhe.localtunnel.me/realtime' #lt --port 8000 --subdomain nzmpqlpmhe

f1=open('./testfile.txt', 'a')
tag = 'swag'

idListing = []
test = ''
lista = []
reactor = None

app = Flask(__name__)

def subscribeToTag(topic):
   print CLIENT_SECRET
   r = api.create_subscription(object = 'tag',
                            object_id = topic,
                            aspect = 'media',
                            callback_url = CALLBACK_TUNNEL,
                            client_id = CLIENT_ID,
                            client_secret = CLIENT_SECRET)
							
   
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
  #tag_search,next_tag = api.tag.search(q=tag)
  tagged_media, next_ = api.tag_recent_media(tag_name=tag, count=amount)
  for media in tagged_media:
     id = media.id
     #img_url= media.images['standard_resolution'].url
     media_link = media.link #linkki paivitykseen
     shortcode = media_link.split("/")[4]
     idListing.append(shortcode)
  return idListing

  
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
       #reactor.register_callback(subscriptions.SubscriptionType.TAG, parse_update)
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

#tekee subscription-toiminnon n. 3 sekunnin kuluttua flask-sovelluksen kaynnistyttya
def doSubscribe():
    print "Subscription process starting"
    time.sleep(3)
    subscribeToTag('swag')
    #global reactor
    #reactor = subscriptions.SubscriptionsReactor()
    #reactor.register_callback(subscriptions.SubscriptionType.TAG, parse_update)
    print 'Subscription process ended'
	
def startApp():
    global app
    app.run(debug=True, port=8000)

reactor = subscriptions.SubscriptionsReactor()

if __name__ == '__main__':
   server = Process(target=startApp)
   server.start()
   sub = Process(target=doSubscribe)
   sub.start()

