import couchdb
import csv
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


consumer_key = "fx8DdDJ72wJfygl89KMFuJglK"
consumer_secret = "nbty0xkOPR6vzkrchHPI9PxStppGj0i92RVdGCgolihMxhF9zp"
access_token = "1206790807-Qk3tsBTAnlFv0ntcQMAWS6jy4j0cNFitUBDHFwt"
access_token_secret = "AkKsz3McpIXSmsrEPVKc27jmMsfUSRIlwIaN2pW7AjnrN"

couch = couchdb.Server()
couch = couchdb.Server('http://admin:admin@localhost:5984/')
db = couch['tweets']



class listener(StreamListener):

  def on_data(self, data):
    all_data = json.loads(data)
    if all_data['lang'] == 'en':
      print(all_data['text'])
      tweet = {}
      tweet_id = all_data["id"]
      tweet['text'] = all_data["text"]
      tweet['user'] = all_data["user"]["name"]
      geo = all_data["geo"]
      if geo != None:
        tweet['lat'] = all_data["geo"]['coordinates'][0]
        tweet['long'] = all_data["geo"]['coordinates'][1]
        db[str(tweet_id)] = tweet
        print(tweet)
    return True

  def on_error(self, status):
      print(status)



auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["*"], locations=[143.9,-38.5,146.1,-37.1])

# auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)

# for tweet in tweepy.Cursor(api.search,q="*",lang = "en",geocode="-37.810142,144.964302,150km").items(1000):
#   if tweet.geo != None:
#     print ([tweet.id, tweet.text, tweet.user.name, tweet.geo['coordinates'], tweet.coordinates])

# doc['name'] = "Happy O'Keeffe"
# doc['text'] = "Flinders Street Station @igersmelbourne instamelbourne abcweather #flinderstation #facade… https://t.co/aY2ZdF6YnT"
# doc['lat'] = -37.81807
# doc['long'] = 144.96681
# db['987196365750132736'] = doc

