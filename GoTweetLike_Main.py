#!/usr/bin/env python
# encoding: utf-8

import tweepy
import time
from FetchTweets import tweets_for_username
from AnalyzeText import random_string_with_length

print "Server start at " + str(time.clock())

#Twitter API credentials
twitter_keys = {}
with open("KEYS.txt") as f:
    for line in f:
        name, var = line.split("=")
        twitter_keys[name.strip()] = var.strip()
        
consumer_key = twitter_keys["consumer_key"]
consumer_secret = twitter_keys["consumer_secret"]
access_key = twitter_keys["access_key"]
access_secret = twitter_keys["access_secret"]

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

print "Twitter API Authenticated"

my_username = "@GoTweetLike"

already_done = []
	

#Define Listener
class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		if status.id not in already_done:
			already_done.append(status.id)
			if status.user.id != "706605179911602176" and status.is_quote_status == False and status.retweeted == False:
				user_mentions = status._json["entities"]["user_mentions"]
				if len(user_mentions) >= 2:
					tweeter_screen_name = status.user.screen_name
					user_to_tweet_like = user_mentions[1]
					username_to_tweet_like = user_to_tweet_like["screen_name"]
					
					#Generate and send tweet
					tweets = tweets_for_username(username_to_tweet_like,api)
					new_tweet = random_string_with_length(15,tweets)
					full_tweet = "@%s @%s: %s" % (tweeter_screen_name, username_to_tweet_like, new_tweet)
					api.update_status(status=full_tweet)
					
					print "Tweeting: %s" % full_tweet
				
			
			
	def on_error(self, status_code):
		print "Error: %d" % status_code
		if status_code == 420:
			return False
# 			print "sleeping..."
# 			time.sleep(60*15)
# 			start_server()
		else:
			start_server()

def start_server():
	my_stream_listener = MyStreamListener()
	my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)
	print "Creating stream..."
	my_stream.filter(track=['@GoTweetLike'])
	
start_server()





	