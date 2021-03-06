import time
import couchdb
import json

COUCHDB_ADDRESS = 'http://admin:admin@localhost:5984/'
COUCHDB_TWEETS_DBNAME = 'preprocess_twitter'
GEO_DBNAME = 'geo_db'

couch = couchdb.Server()
couch = couchdb.Server(COUCHDB_ADDRESS)

if COUCHDB_TWEETS_DBNAME in couch:
    db = couch[COUCHDB_TWEETS_DBNAME]
else:
    db = couch.create(COUCHDB_TWEETS_DBNAME)

if GEO_DBNAME in couch:
    geodb = couch[GEO_DBNAME]
else:
    geodb = couch.create(GEO_DBNAME)

def tweets_geo_sentiment_count(db, geodb):
  tweet_geo_sentment_dict = {}
  for item in db.view('sentiment/sa2_sentiment', stale="update_after", group=True):
    print(item)
    sa2_main = item.key[0]
    if sa2_main != None:
      sentiment = item.key[1]
      doc = geodb[sa2_main]
      doc[sentiment] = item.value
      try:
        geodb[sa2_main] = doc
      except:
        pass
      temp = tweet_geo_sentment_dict.get(sa2_main, {})
      temp[sentiment] = item.value
      tweet_geo_sentment_dict[sa2_main] = temp
  return tweet_geo_sentment_dict

def tweets_geo_sentiment_rate(geodb, tweet_geo_sentment_dict):
  for key, value in tweet_geo_sentment_dict.items():
    temp = {}
    doc = geodb[key]
    temp['SA2_MAIN16'] = key
    temp['pos'] = value.get('pos', 0)
    temp['neu'] = value.get('neu', 0)
    temp['neg'] = value.get('neg', 0)
    doc['pos_rate'] = float(temp['pos'])/max((temp['pos']+temp['neu']+temp['neg']),1)
    try:
      geodb[key] = doc
    except:
      pass

if __name__ == '__main__':
  while True:
    tweet_geo_sentment_dict = tweets_geo_sentiment_count(db, geodb)
    tweets_geo_sentiment_rate(geodb, tweet_geo_sentment_dict)
    time.sleep(10*60)
