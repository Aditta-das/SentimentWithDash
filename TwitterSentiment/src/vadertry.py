import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
ckey = "DkxpqWmgpvn30bZB25JrwwE90"
APISecret = "PiuIQU7mjSgkjUQQu3rCXnqwlAhitNrwakimx5NAv0TGyT6gL6"

Access_token = "1389226167996010501-sqoxNOay1BkI1Nlr5T9gDPzcjIYs95"
Access_Token_Secret = "wXkodqLycBo60uCXAq6fm5FN3dZR02fmmKut7wbtrk6kw"

auth = OAuthHandler(consumer_key=ckey, consumer_secret=APISecret)
auth.set_access_token(key=Access_token, secret=Access_Token_Secret)

api = tweepy.API(auth)
public_tweet = api.search("Trump")

for tweet in public_tweet:
	print(tweet)