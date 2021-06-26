from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json 
from unidecode import unidecode
from dateutil.parser import parse
import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import os, time
import sqlite3
import random
import pandas as pd
from threading import Lock, Timer, RLock, Event
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_analyze(sentence):
	sid_obj = SentimentIntensityAnalyzer()
	sentiment_dict = sid_obj.polarity_scores(sentence)
	return sentiment_dict

default_path = os.path.join(os.path.dirname(__file__), "twitter.db")
con = sqlite3.connect(default_path, check_same_thread=False)
cur = con.cursor()

def create_database():
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS sentiment (id INTEGER PRIMARY KEY AUTOINCREMENT, create_at REAL, tweet TEXT, score REAL, sentiment TEXT)")
        con.commit()
    except Exception as e:
        print(e)


create_database()

lock = Lock()

ckey = #
APISecret = #

Access_token = #
Access_Token_Secret = #


class listener(StreamListener):
	lock = None
	data = []
	def __init__(self, lock):
		self.save_in_database()
		self.lock = lock
		self.stop_words = set(stopwords.words("english"))
		
		super().__init__()
	
	def save_in_database(self):
		Timer(interval=1, function=self.save_in_database).start()
		with Lock():
			if len(self.data):
				cur.execute("BEGIN TRANSACTION")
				try:
					cur.executemany('INSERT INTO sentiment(create_at, tweet, score, sentiment) VALUES (?, ?, ?, ?)', self.data)
				except:
					pass

				con.execute("COMMIT")
				self.data = []

	def on_data(self, data):
		try:
			data = json.loads(data)
			# print(data)
			if 'truncated' not in data:
				return True

			if data["truncated"]:
				tweet = unidecode(data["extended_tweet"]["full_text"])
			else:
				tweet = unidecode(data["text"])
			word_tokens = word_tokenize(tweet)
			filtered_sentence = " ".join([w.lower() for w in word_tokens if w.lower() not in self.stop_words])
			# created = parse(data["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
			created = data["timestamp_ms"]
			sentiment_dict = sentiment_analyze(sentence=filtered_sentence)
			comp = sentiment_dict["compound"]
			if comp > 0:
				sentiment = "Positive"
			elif comp < 0:
				sentiment = "Negative"
			else:
				sentiment = "Neutral"
			with self.lock:
				self.data.append((created, filtered_sentence, comp, sentiment))
			print(self.data)
		except Exception as e:
			print(str(e)) 
		return True


	def on_error(self, status):
		print(status)



while True:
	try:
		auth = OAuthHandler(consumer_key=ckey, consumer_secret=APISecret)
		auth.set_access_token(key=Access_token, secret=Access_Token_Secret)
		twitterStream = Stream(auth, listener(lock))
		twitterStream.filter(track=["a", "e", "i", "o", "u"])
		# twitterStream.filter(track=["Clippers"])
	except Exception as e:
		print(str(e))
		time.sleep(5)