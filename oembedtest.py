import oembed
import pprint
import json
import requests
import urllib

str = "9nlqe2OrT1"
testi = urllib.quote(str)
str2 = "http://instagr.am/p/9nlqe2OrT1"

consumer = oembed.OEmbedConsumer()
endpoint = oembed.OEmbedEndpoint('http://api.instagram.com/oembed', 'http://instagr.am/p/*')
consumer.addEndpoint(endpoint)
response = consumer.embed(str2)

#print type(response)
pprint.pprint(response.getData())
#print response['html']
print response['url']