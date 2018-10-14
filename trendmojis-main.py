##############################################
## Authors: Dorian HENAULT and Alexis SEGURA##
## Email: alex.segura06@gmail.com ############
## Status: In development #################### 
## Version: 0.1 ##############################
##############################################

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import time
import json
import emoji
import datetime
import database

with open('credentials.json', 'r') as f:
    credentials = json.load(f)

ckey=credentials["twitter"]['ckey']
csecret=credentials["twitter"]['csecret']
atoken=credentials["twitter"]['atoken']
asecret=credentials["twitter"]['asecret']

###### Authentification and connexion to the twitter API ######
class listener(StreamListener):
    def on_data(self, data):
        jsonTweet = json.loads(data)
        print(jsonTweet["text"])
        time.sleep(5)
        return(True)

    def on_error(self, status):
        print(status)

###### Process tweets for a given keyword ######
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
    emoj = max(dicCountryEmoji, key=dicCountryEmoji.get)
    print("The most used emoji in tweets for", keyword,"is :",emoj)
    print("Number of pages prosseced : ", page_count)
    return emoj

###### Trends by country ######
def retrieve_trend(location, todayDate, numberOfTrend):
    trends = api.trends_place("610264")
    counter = 0
    trendDic = {}
    for i in range(0,len(trends[0]['trends'])) :
        counter+=1
        trend = trends[0]['trends'][i]['name']
        print("Searching emoji for the trend: ", trend)
        emoj = process_tweets(trend, todayDate)
        print("\n")
        trendDic[trend] = emoj
        if(counter == numberOfTrend):
            return trendDic

###### Write the tweet ######
def write_tweet(trendDic):
    space = "   - "
    tweet="The most used emoji for each trend in France : \n"
    for trend, emoj in trendDic.items():
        tweet += space
        tweet += trend + " : " + emoj
        tweet += "\n"
    return tweet

#Connection
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# Curso Mode
api = tweepy.API(auth, wait_on_rate_limit=True) 

#WOEID
FRANCE = "23424819"
EU = "24865675"

#Process
now = datetime.datetime.now()
todayDate = now.strftime("%Y-%m-%d")
start_time = time.time()
trendDic = retrieve_trend(EU, todayDate, 8)
tweet = write_tweet(trendDic)
scriptDuration = time.time() - start_time
print(scriptDuration)
print("\n"+tweet)
