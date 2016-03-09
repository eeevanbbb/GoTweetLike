#!/usr/bin/env python
# encoding: utf-8

import tweepy
import time
from FetchTweets import tweets_for_username
from AnalyzeText import generate_tweet_with_max_char_length
from AnalyzeText import generate_tweet_with_max_char_length_and_seed
from RequestParser import get_tweet_type
from AnalyzeText import generate_stats_for_tweets

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
	

#Send Error Message
def send_error_message(user_id):
	print "Invalid Request"
	#api.send_direct_message(user_id,text="Sorry, the format of your tweet was invalid. Please see the usage instructions here: https://github.com/eeevanbbb/GoTweetLike")

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
					max_chars = 140 - (len(tweeter_screen_name) + len(username_to_tweet_like) + 5)
					tweets = tweets_for_username(username_to_tweet_like,api)
					tweet_type = get_tweet_type(status.text)
					if tweet_type == "Invalid":
						send_error_message(status.user.id)
					else:
						new_tweet = "If you're seeing this text, something is wrong."
						if tweet_type == "Standard":
							new_tweet = generate_tweet_with_max_char_length(max_chars,tweets)
						elif tweet_type.startswith("Topic:"):
							topic = tweet_type.split()[1]
							new_tweet = generate_tweet_with_max_char_length_and_seed(max_chars,topic,tweets)
							if new_tweet == topic:
								#The topic was not in the frequency table
								new_tweet = "I have nothing to say about " + topic
						elif tweet_type == "Stats":
							new_tweet = generate_stats_for_tweets(tweets)
							
							
						full_tweet = "@%s @%s: %s" % (tweeter_screen_name, username_to_tweet_like, new_tweet)
						api.update_status(status=full_tweet,in_reply_to_status_id=status.id)
						print "Tweeting: %s" % full_tweet
						
						#Follow both users
						api.create_friendship(tweeter_screen_name)
						if username_to_tweet_like.lower() != my_username.lower():
							api.create_friendship(username_to_tweet_like)
				else:
					if status.text.lower().startswith("@gotweetlike"):
						send_error_message(status.user.id)
				
			
			
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





	