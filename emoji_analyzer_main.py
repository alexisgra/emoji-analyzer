from tweepy import Stream
from tweepy import OAuthHandler
import tweepy
from tweepy.streaming import StreamListener
import time
import json
import emoji


#consumer key, consumer secret, access token, access secret.
ckey="XXXX"
csecret="XXXX"
atoken="XXXX"
asecret="XXXX"

#Authentification and connexion to the twitter API
class listener(StreamListener):
    def on_data(self, data):
        jsonTweet = json.loads(data)
        print(jsonTweet["text"])
        time.sleep(5)
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# Stream Mode
# twitterStream = Stream(auth, listener())
# twitterStream.filter(track=["Equipe de France"])
#tweets = api.search(q="place:%s" % france, lang="fr", count=100, tweet_mode="extended")

# Curso Mode
api = tweepy.API(auth, wait_on_rate_limit=True)
#Geo code
france = 'f3bfc7dcc928977f'

#Topic
query = "#Malcom"
dicCountryEmoji = {}
page_count=0
for page in tweepy.Cursor(api.search, q=query, lang="fr", since="2018-07-18", count=100,tweet_mode="extended").pages():
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
print("The most used emoji in tweets for", query,"is :",max(dicCountryEmoji, key=dicCountryEmoji.get))

###### Tendances by country ######
# trends = api.trends_place("610264")
# for i in range(0,len(trends[0]['trends'])) :
#     print(trends[0]['trends'][i]['name'])
#     #print("\n")