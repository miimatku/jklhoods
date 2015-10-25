from flask import Flask
from instagram import client

CLIENT_ID='efe6cccbd3ac4e75b842c957e954c569'
CLIENT_SECRET='bdadba8a4b274b45bdfcb306cfd6b120'
ACCESS_TOKEN='1442727277.1677ed0.ed44f2c97aa24fd1a559e80dbef8d6a0'


def getImageURLs():
   api = client.InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token= ACCESS_TOKEN)
   popular_media = api.media_popular(count=20)
   return popular_media
   
def subscribe():
   api = client.InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token= ACCESS_TOKEN)
   sub = api.create_subscription(object='tag', object_id='jyvaeskylae', aspect='media', callback_url='https://shielded-wave-4959.herokuapp.com/callback')

#subscribe()

app = Flask(__name__)

@app.route('/')
def index():
   return getImageURLs()

@app.route('/callback')
return 'kissa'

   
if __name__ == '__main__':
   app.run()
   
   
