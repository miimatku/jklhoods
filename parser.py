try:
    import json
except ImportError:
    import simplejson as json
import urllib, cStringIO
from dateutil.parser import parse

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

#hakee kuvat URL-osoitteiden perusteella
def imagesFromURL(urls):
   images = []
   for url in urls:
      file = cStringIO.StringIO(urllib.urlopen(URL).read())
      img = Image.open(file)
      images.append(img)
   return images

#paivamaaran parsiminen
def parseDate(date):
   return date





#Twitter API:n tarvitsemat tiedot
ACCESS_TOKEN = '3869893516-1jWdaC3do0Dvhyb8TP8C6bvaYPRBMt28ug4aoDW'
ACCESS_SECRET = 'IbEu7Q0an9E3T3wzzrYCIRKqy9T370Xnz4HdHFTcrEfWI'
CONSUMER_KEY = 'kwZuZArqeNhEtP5iFZLbA4tGq'
CONSUMER_SECRET = 'AxHMUj8Am1Z0bTrjg7OlZmIW6S1iCCbCGJj7esvNwsWOkFCxVM'
COUNT = 1

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter = Twitter(auth=oauth)
query = twitter.search.tweets(q='#jyvaeskylae', result_type='recent', count=COUNT)

img_urls = []
tweets = [] #sisakkainen lista [[kayttaja, teksti, kuvan url tai '']]
x = 0
while x < COUNT:
   user = query['statuses'][x]['user']['screen_name']  #tweettaajan kayttajanimi
   date = query['statuses'][x]['created_at']
   text = query['statuses'][x]['text'] #tweetin teksti (escaped)
   url = ''
   
   try:
     url  = query['statuses'][x]['entities']['media'][0]['media_url'] #tweetissa olevan kuvan url
     #print url
     img_urls.append(url)
     tweets.append([user,text,date,url])
   except:
      tweets.append([user,text,date,""])
      x += 1
      continue 
   x += 1

pvm = parseDate(tweets[0][2])
print pvm
#print tweets #testi
#print tweets[0][0] #testi. kayttajanimen tulostus

