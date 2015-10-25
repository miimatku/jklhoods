from flask import Flask,request, Response
from instagram import client, subscriptions
from twisted.internet import reactor
try:
    import json
except ImportError:
    import simplejson as json

CLIENT_ID='efe6cccbd3ac4e75b842c957e954c569'
CLIENT_SECRET='bdadba8a4b274b45bdfcb306cfd6b120'
ACCESS_TOKEN='1442727277.5b9e1e6.71468fed77d14c4fb1d3a41b2644d4de'
COUNT = 1


api = client.InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token= ACCESS_TOKEN)

def getImageURLs():
   popular_media = api.media_popular(count=COUNT)
   return popular_media

def subscribeToTag(wanted_tag):
   sub = api.create_subscription(object='tag', object_id=wanted_tag, aspect='media', callback_url='https://shielded-wave-4959.herokuapp.com/callback')
   
   
def parse_update(update):
   instagram_userid = update['object_id']
   return str(instagram_userid)

app = Flask(__name__)

@app.route('/')
def index():
   lista = getImageURLs()
   #str-funktiolla toimii
   return str(api.list_subscriptions())


#kutsutaan, kun uutta jyvaskyla-tagilla merkittya instagram-postia tulee
@app.route('/callback')
def callback():  
   mode         = request.values.get('hub.mode')
   challenge    = request.values.get('hub.challenge')
   verify_token = request.values.get('hub.verify_token')
   return str(mode) + "   " + str(challenge) + "   " + str(verify_token)
   
   if challenge: 
       return Response(challenge)
   else:
       reactor = subscriptions.SubscriptionsReactor()
       reactor.register_callback(subscriptions.SubscriptionType.TAG, parse_update)

       x_hub_signature = request.headers.get('X-Hub-Signature')
       raw_response    = request.data
       try:
           reactor.process(CLIENT_SECRET, raw_response, x_hub_signature)
       except subscriptions.SubscriptionVerifyError:
           logging.error('Instagram signature mismatch')
   return Response('Parsed instagram')
   

if __name__ == '__main__':
   app.run(debug=True)
   reactor.run()
   subscribeToTag("jyvaeskylae")
   
   
