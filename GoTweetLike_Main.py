#!/usr/bin/env python
# encoding: utf-8

import tweepy
import time
import os.path
import csv
import re	
import operator
from random import randint
import sys

control_string = "***///END///***"

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





#Sanitize Tweets
def sanitize_tweet(tweet):
	without_url = re.sub(r"(?:\@|https?\://)\S+", "", tweet)
# 	lower_case = without_url.lower()
	return without_url
	
def sanitize_tweets(tweets):
	sanitized = []
	for tweet in tweets:
		sanitized.append(sanitize_tweet(tweet))
	return sanitized

#Fetch tweets
def tweets_for_username(username):
	filepath = 'tweets/%s_tweets.csv' % username
	if not os.path.isfile(filepath):
		#initialize a list to hold all the tweepy Tweets
		alltweets = []	
	
		#make initial request for most recent tweets (200 is the maximum allowed count)
		new_tweets = api.user_timeline(screen_name = username,count=200)
	
		#save most recent tweets
		alltweets.extend(new_tweets)
	
		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
	
		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			print "getting tweets before %s" % (oldest)
		
			#all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(screen_name = username,count=200,max_id=oldest)
		
			#save most recent tweets
			alltweets.extend(new_tweets)
		
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
		
			print "...%s tweets downloaded so far" % (len(alltweets))
	
		#transform the tweepy tweets into a 2D array that will populate the csv	
		outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
		#write the csv	
		with open('tweets/%s_tweets.csv' % username, 'wb') as f:
			writer = csv.writer(f)
			#writer.writerow(["id","created_at","text"])
			writer.writerows(outtweets)
	
	#Read tweets from the csv
	tweets = []
	with open('tweets/%s_tweets.csv' % username, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			tweet = row[2]
			tweets.append(tweet)
			
	tweets = sanitize_tweets(tweets)	
	return tweets



#Analysis
def get_successor_histagram(tweets):
	dict = {}
	for tweet in tweets:
		rgx = re.compile("(#*\w[\w']*\w|\w).?")
		words = rgx.findall(tweet)
		for i in range(0,len(words)):
			word = words[i]
			next_word = control_string
			if i+1 < len(words):
				next_word = words[i+1]
			if word != "" and next_word != "":
				if word not in dict:
					dict[word] = {}
				successor_dict = dict[word]
				if next_word in successor_dict:
					successor_dict[next_word] += 1
				else:
					successor_dict[next_word] = 1
	return dict
	
	
def choice_from_weighted_dict(dict):
	total = 0
	for word, freq in dict.iteritems():
		total += freq
	random_int = randint(0,total)
	upto = 0
	for word, freq in dict.iteritems():
		if upto + freq >= random_int:	
			return word
		upto += freq
	assert False, "Random Int Too High"		

	
def get_next_word(word,tweets):
	successor_histagram = get_successor_histagram(tweets)
	if word not in successor_histagram:
		return ""
	else:
		successor_dict = successor_histagram[word]
		next_word = choice_from_weighted_dict(successor_dict)
		if next_word == control_string:
			return ""
		else:
			return next_word
				
	
def random_string_from_seed_with_length(seed,length,tweets):
	running_length = 1
	string = seed
	should_continue = True
	last_word = seed
	while running_length < length and should_continue:
		next_word = get_next_word(last_word,tweets)
		if next_word != "":
			string += " "
			string += next_word
			last_word = next_word
			running_length += 1
		else:
			should_continue = False
	return string
	
def get_starting_word_histagram(tweets):
	dict = {}
	for tweet in tweets:
		words = re.split('\W+', tweet)
		if len(words) > 0:
			word = words[0]
			if word != "" and word != "RT":
				if word in dict:
					dict[word] += 1
				else:
					dict[word] = 1
	return dict

def random_string_with_length(length,tweets):
	seed = choice_from_weighted_dict(get_starting_word_histagram(tweets))
	return random_string_from_seed_with_length(seed,length,tweets)
	
	
	

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
					print "@%s @%s: tweet goes here..." % (tweeter_screen_name, username_to_tweet_like)
					#Do the stuff...
					tweets = tweets_for_username(username_to_tweet_like)
					new_tweet = random_string_with_length(15,tweets)
					full_tweet = "@%s @%s: %s" % (tweeter_screen_name, username_to_tweet_like, new_tweet)
					api.update_status(full_tweet)	
				
			
			
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





	