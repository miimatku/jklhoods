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

def subscribeToTag(topic):
   r = api.create_subscription(object = 'tag',
                            object_id = topic,
                            aspect = 'media',
                            callback_url = 'https://shielded-wave-4959.herokuapp.com/callback',
                            client_id = CLIENT_ID,
                            client_secret = CLIENT_SECRET
)
   
def parse_update(update):
   instagram_userid = update['object_id']
   print str(instagram_userid)

app = Flask(__name__)

@app.route('/')
def index():
   lista = getImageURLs()
   #str-funktiolla toimii
   return str(api.list_subscriptions())


#kutsutaan, kun uutta jyvaskyla-tagilla merkittya instagram-postia tulee
@app.route('/callback')
def import_instagram_rt(request, slug):
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
            fetch_data(slug, update["object_id"])   
   

   
#reactor versio
@app.route('/callback2')
def callback2():  
   mode         = request.values.get('hub.mode')
   challenge    = request.values.get('hub.challenge')
   verify_token = request.values.get('hub.verify_token')
   
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
   
   
