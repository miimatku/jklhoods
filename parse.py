try:
    import json
except ImportError:
    import simplejson as json
import urllib, cStringIO

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

#Twitter API:n tarvitsemat tiedot
ACCESS_TOKEN = '3869893516-1jWdaC3do0Dvhyb8TP8C6bvaYPRBMt28ug4aoDW'
ACCESS_SECRET = 'IbEu7Q0an9E3T3wzzrYCIRKqy9T370Xnz4HdHFTcrEfWI'
CONSUMER_KEY = 'kwZuZArqeNhEtP5iFZLbA4tGq'
CONSUMER_SECRET = 'AxHMUj8Am1Z0bTrjg7OlZmIW6S1iCCbCGJj7esvNwsWOkFCxVM'
COUNT = 30

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter = Twitter(auth=oauth)
query = twitter.search.tweets(q='#jyvaeskylae', result_type='recent', count=COUNT)

img_urls = []

x = 0
while x < COUNT:
   ent =  query['statuses'][x]['entities']
   try:
      print ent['media'][0]['media_url']
      img_urls.append(ent['media'][0]['media_url'])
   except:
      x += 1
      continue
   x += 1

print len(img_urls) #testi

#hakee kuvat URL-osoitteiden perusteella
def imagesFromURL(urls):
   images = []
   for url in urls:
      file = cStringIO.StringIO(urllib.urlopen(URL).read())
      img = Image.open(file)
      images.append(img)
   return images

