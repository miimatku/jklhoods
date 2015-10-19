
from instagram.client import InstagramAPI
from instagram import client,subscriptions

try:
    import json
except ImportError:
    import simplejson as json

from random import randint
import sys
from collections import OrderedDict


client_id = 'efe6cccbd3ac4e75b842c957e954c569'
client_secret = 'c1c4d5370b664b2cacf4b51c15e30c14'
access_token = '1442727277.1677ed0.ed44f2c97aa24fd1a559e80dbef8d6a0'
client_ip = '127.0.0.1'

media_all_ids = []

api = InstagramAPI(client_id=client_id, client_secret=client_secret, client_ips= client_ip,access_token= access_token) 

query, next_ = api.tag_recent_media(tag_name='jyvaeskylae', count=10)

"""def getMedia():
    lst = []
    for media in query:
      lst.append(media.images['standard_resolution'].url)
    return lst
"""
"""
popular_media = api.media_popular(count=10)
for media in popular_media:
    print media.images['standard_resolution'].url
   """

for media in query:
    print media.images['standard_resolution'].url


