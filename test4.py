#!/usr/bin/python
from flask import Flask,request, Response,redirect,url_for
from instagram import client, subscriptions
from twisted.internet import reactor
import simplejson
from django.http import HttpResponse
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

f1=open('./testfile', 'a')

idListing = ['asd']
test = ''

app = Flask(__name__)

def subscribeToTag(topic):
   r = api.create_subscription(object = 'tag',
                            object_id = topic,
                            aspect = 'media',
                            callback_url = CALLBACK_TUNNEL,
                            client_id = CLIENT_ID,
                            client_secret = CLIENT_SECRET)
							
   
def parse_update(update):
   instagram_userid = update['object_id']
   id =  str(instagram_userid)
   lista.append('asda')
   return redirect(url_for('showInstagram'))
   
def getImageURLs():
   popular_media = api.media_popular(count=COUNT)
   return popular_media


@app.route('/showInstagram')
def showInstagram():
   global idListing
   return str(len(idListing))
   

@app.route('/', methods=['GET','POST'])
def index():
   #subscribeToTag('swag') 
   print 'ad'
   lista = getImageURLs()
   #str-funktiolla toimii
   #global sub
   return str(lista[0])
   
   
"""
@app.before_first_request
def _run_on_start():
   subscribeToTag('swag') 
"""
   
"""
#kutsutaan, kun uutta jyvaskyla-tagilla merkittya instagram-postia tulee
@app.route('/callback3', methods=['POST','GET'])
def sub_callback(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        challenge = request.GET.get("hub.challenge")
        verify_token = request.GET.get("hub.verify_token")
        if challenge:
            return HttpResponse(challenge, mimetype='text/html')
        else:
            return HttpResponse("test", mimetype='text/html')
    else:
        x_hub_signature=''
        if request.META.has_key('HTTP_X_HUB_SIGNATURE'):
            x_hub_signature = request.META['HTTP_X_HUB_SIGNATURE']
        raw_response = request.raw_post_data
        data = simplejson.loads(raw_response)
        for update in data:
            parse_update(update)   
"""

"""	
@app.route('/callback', methods=['POST','GET'])
def kokeilu(request):
   code = request.args.get('hub.challenge')
   mode = request.args.get("hub.mode")
   verify_token = request.args.get("hub.verify_token")
   if code:
      return Response(code)
   else:
      x_hub_signature = request.headers.get('X-Hub-Signature')
      raw_response = request.data
      try:
           parse_update(simplejson.loads(raw_response)
      except:
           logging.error('Instagram signature mismatch')
		   pass
   return Response('Parsed instagram')
"""
   

#reactor versio
@app.route('/realtime', methods=['POST','GET'])
def callback(): 
   global test
   if request.method == 'GET':
      mode         = request.values.get('hub.mode')
      challenge    = request.values.get('hub.challenge')
      verify_token = request.values.get('hub.verify_token')
      print >> f1, mode
      print >> f1, challenge
      print >> f1, verify_token
      if challenge:
         return Response(challenge)
   else:
       reactor = subscriptions.SubscriptionsReactor()
       reactor.register_callback(subscriptions.SubscriptionType.TAG, parse_update)
	   
       x_hub_signature = request.headers.get('X-Hub-Signature')
       raw_response    = request.data
       data = simplejson.loads(raw_response[0])
       print >> f1, data
       try:
           reactor.process(CLIENT_SECRET, data, x_hub_signature)
       except subscriptions.SubscriptionVerifyError:
           logging.error('Instagram signature mismatch')
   return Response('SUP') #ei tarvitse vastausta.

api = client.InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token= ACCESS_TOKEN) 

def doSubscribe():
    print "Subscription process starting"
    time.sleep(3)
    subscribeToTag('swag')
    print 'Subscription process ended'
	
def startApp():
    global app
    app.run(debug=True, port=8000)
	

if __name__ == '__main__':
   server = Process(target=startApp)
   server.start()
   sub = Process(target=doSubscribe)
   sub.start()
   #reactor.run()
