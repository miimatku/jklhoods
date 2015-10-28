from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sqlite3 as sql3
import time
import json
#import sys

#consumer key, consumer secret, access token, access secret.
ckey="kwZuZArqeNhEtP5iFZLbA4tGq"
csecret="AxHMUj8Am1Z0bTrjg7OlZmIW6S1iCCbCGJj7esvNwsWOkFCxVM"
atoken="3869893516-1jWdaC3do0Dvhyb8TP8C6bvaYPRBMt28ug4aoDW"
asecret="IbEu7Q0an9E3T3wzzrYCIRKqy9T370Xnz4HdHFTcrEfWI"


con = sql3.connect("tweets.db")

cur = con.cursor()


class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        id = all_data["id_str"]
        time = all_data["created_at"]
        name = all_data["user"]["name"]
        screen_name = all_data["user"]["screen_name"]
        tweet = all_data["text"]

        cur.execute("INSERT INTO tweets (id, time, username, screen_name, tweet) VALUES (?, ?, ?, ?, ?)",
            (id, time, name, screen_name, tweet))

        con.commit()

        print((screen_name, name, time))
        
        return True

    def on_error(self, status):
    	if status == 420:
    		#returning False in on_data disconnects the stream
    		return False
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, Listener())
twitterStream.filter(track=["swag"])

#def runStream():
#    auth = OAuthHandler(ckey, csecret)
#    auth.set_access_token(atoken, asecret)
#    twitterStream = Stream(auth, listener())
#    twitterStream.filter(track=["Finland"])

