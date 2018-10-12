from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import time
import json
import emoji
import datetime

logs = open("logs.txt", "r") 

#consumer key, consumer secret, access token, access secret.
ckey=logs.readline()[:-1]
csecret=logs.readline()[:-1]
atoken=logs.readline()[:-1]
asecret=logs.readline()

#Authentification and connexion to the twitter API
class listener(StreamListener):
    def on_data(self, data):
        jsonTweet = json.loads(data)
        print(jsonTweet["text"])
        time.sleep(5)
        return(True)

    def on_error(self, status):
        print(status)

#Process_tweets
def process_tweets(keyword, date):
    dicCountryEmoji = {}
    page_count=0
    for page in tweepy.Cursor(api.search, q=keyword, lang="fr", since=date, count=100,tweet_mode="extended").pages():
        page_count+=1
        for tweet in page : 
            allchars = [str for str in tweet.full_text]
            for c in allchars :
                if c in emoji.UNICODE_EMOJI and c not in dicCountryEmoji : 
                    dicCountryEmoji[c]=1
                elif c in emoji.UNICODE_EMOJI : 
                    dicCountryEmoji[c]+=1
        if page_count >= 100:
            break
    print("The most used emoji in tweets for", keyword,"is :",max(dicCountryEmoji, key=dicCountryEmoji.get))
    print("Number of pages prosseced : ", page_count)

###### Tendances by country ######
def retrieve_trend(location, date, numberOfTrend):
    trends = api.trends_place("610264")
    counter = 0
    for i in range(0,len(trends[0]['trends'])) :
        counter+=1
        trend = trends[0]['trends'][i]['name']
        print("Search emojis for the trend : " + trend + "\n")
        process_tweets(trend, date)
        print("\n")
        if(counter == numberOfTrend):
            return

#Connection
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# Curso Mode
api = tweepy.API(auth, wait_on_rate_limit=True) 

#WOEID
FRANCE = "23424819"

#Process
now = datetime.datetime.now()
todayDate = now.strftime("%Y-%m-%d")
start_time = time.time()
retrieve_trend(FRANCE, todayDate, 8)
scriptDuration = time.time() - start_time
print(scriptDuration)