#!/usr/bin/env python
# encoding: utf-8

import tweepy
import time
import sys
import math
from FetchTweets import tweets_for_username
from AnalyzeText import generate_tweet_with_max_char_length
from AnalyzeText import generate_tweet_about_topic_with_max_char_length
from RequestParser import get_tweet_type
from AnalyzeText import generate_stats_for_tweets
from AnalyzeText import generate_advanced_stats_for_tweets
from AnalyzeText import get_longest_word_tweet_for_tweets
from AnalyzeText import generate_rant


#Prepend time to all log output (http://stackoverflow.com/questions/4883789/adding-a-datetime-stamp-to-python-print)
old_out = sys.stdout
class new_out:
    nl = True

    def write(self, x):
        """Write function overloaded."""
        if x == '\n':
            old_out.write(x)
            self.nl = True
        elif self.nl:
            old_out.write('[%s] %s' % (time.ctime(), x))
            self.nl = False
        else:
            old_out.write(x)

sys.stdout = new_out()


print "Script started"

#Blacklisted accounts
blacklisted = []
with open("BLACKLIST.txt") as blacklist_file:
	for line in blacklist_file:
		blacklisted.append(line)

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

my_username = "GoTweetLike"

already_done = []


#Send Error Message
def send_error_message(user_id):
	print "Invalid Request"
	#api.send_direct_message(user_id,text="Sorry, the format of your tweet was invalid. Please see the usage instructions here: https://github.com/eeevanbbb/GoTweetLike")

#Define Listener
#Credit to: https://github.com/benmckibben/Twanslate/blob/master/Twanslate.py
class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		if status.id not in already_done:
			already_done.append(status.id)
			if status.user.id != "706605179911602176" and status.is_quote_status == False and status.retweeted == False:
				print "Processing tweet: %s" % status.text
				user_mentions = status._json["entities"]["user_mentions"]
				if len(user_mentions) >= 2:
					tweeter_screen_name = status.user.screen_name
					user_to_tweet_like = user_mentions[1]
					username_to_tweet_like = user_to_tweet_like["screen_name"]
					if username_to_tweet_like in blacklisted:
						print "The user %s is blacklisted" % username_to_tweet_like
						return

					#Generate and send tweet
					max_chars = 140 - (len(tweeter_screen_name) + len(username_to_tweet_like) + 5)
					tweets = tweets_for_username(username_to_tweet_like,api,False)
					tweet_type = get_tweet_type(status.text)
					if tweet_type == "Invalid":
						send_error_message(status.user.id)
					else:
						new_tweet = "If you're seeing this text, something is wrong."
						if tweet_type == "Standard":
							new_tweet = generate_tweet_with_max_char_length(max_chars,tweets)
						elif tweet_type == "Update":
							tweets = tweets_for_username(username_to_tweet_like,api,True)
							new_tweet = generate_tweet_with_max_char_length(max_chars,tweets)
						elif tweet_type.startswith("Topic:"):
							topic = tweet_type.split()[1]
							new_tweet = generate_tweet_about_topic_with_max_char_length(topic,max_chars,tweets)
							if new_tweet == topic:
								#The topic was not in the frequency table
								new_tweet = "I have nothing to say about " + topic
						elif tweet_type == "Stats":
							new_tweet = generate_stats_for_tweets(tweets)
						elif tweet_type == "AdvancedStats":
							new_tweet = generate_advanced_stats_for_tweets(tweets)
						elif tweet_type == "LongestWord":
							new_tweet = get_longest_word_tweet_for_tweets(tweets)
						elif tweet_type == "Rant":
							new_tweet = generate_rant(600,1000,tweets)


						address = "@%s @%s: " % (tweeter_screen_name, username_to_tweet_like)
						full_tweet = address + new_tweet

						outgoing_tweets = []

						#Okay, this will take some explaining
						#If the full tweet is <= 140 chars, perfect, we're done
						#Otherwise, we have to divide it up into separate tweets
							#Each tweet must have the address to the users,
							#As well as an indicator of which tweet it is in the list
							#This means we have to calculate the overhead beforehand
							#And divide accordingly, until there are no more chars left

						if len(full_tweet) <= 140:
							outgoing_tweets.append(full_tweet)
						else:
							addressLength = len(address)
							countLength = len("(?/?) ") #NOTE: Only supports up to 9 tweets
							overheadLength = addressLength + countLength
							maxTextLength = 140 - overheadLength
							tweetNumber = 0
							totalTweets = int(math.ceil(float(len(new_tweet)) / float(maxTextLength)))
							while len(new_tweet) > 0:
								tweetNumber += 1
								partialTweet = address + "(%d/%d) " % (tweetNumber,totalTweets) + new_tweet[:maxTextLength]
								outgoing_tweets.append(partialTweet)
								new_tweet = new_tweet[maxTextLength:]


						#Send the tweets
						for outgoing_tweet in outgoing_tweets:
							api.update_status(status=outgoing_tweet,in_reply_to_status_id=status.id)
							print "Tweeting: %s" % outgoing_tweet

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
	try:
		my_stream.filter(track=['@GoTweetLike'])
	except AttributeError as e: # ignore error in Tweepy library (see here: https://github.com/tweepy/tweepy/issues/576)
		print "Caught AttributeError, Restarting server (%s)" % e.message
		start_server()

start_server()
