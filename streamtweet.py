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


class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        
        username = all_data["user"]["screen_name"]
        
        cur.execute("INSERT INTO taula (time, username, tweet) VALUES (?, ?, ?)",
            (time.time(), username, tweet))

        con.commit()

        print((username,tweet))
        
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Finland"])

#def runStream():
#    auth = OAuthHandler(ckey, csecret)
#    auth.set_access_token(atoken, asecret)
#    twitterStream = Stream(auth, listener())
#    twitterStream.filter(track=["Finland"])

