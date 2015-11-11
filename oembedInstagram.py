import oembed

def getOEmbed(shortcode):
	address = "http://instagr.am/p/" + shortcode[0]
 	script_url= '<script async defer src="http://platform.instagram.com/en_US/embeds.js"></script>' 
 	consumer = oembed.OEmbedConsumer()
 	endpoint = oembed.OEmbedEndpoint('http://api.instagram.com/oembed', 'http://instagr.am/p/*')
 	consumer.addEndpoint(endpoint)
 	try:
	 	response = consumer.embed(address)
 	except Exception, e:
 		return None
 	return response['html'].split('<script')[0]