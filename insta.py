from instagram.client import InstagramAPI

client_id = 'efe6cccbd3ac4e75b842c957e954c569'
client_secret = 'c1c4d5370b664b2cacf4b51c15e30c14'
access_token = '1442727277.1677ed0.ed44f2c97aa24fd1a559e80dbef8d6a0'
client_ip = '127.0.0.1'

api = InstagramAPI(client_id=client_id, client_secret=client_secret, client_ips= client_ip,access_token= access_token) 

query= api.tag_recent_media(tag_name='Jyvaeskylae', count=30)
print query[0]
