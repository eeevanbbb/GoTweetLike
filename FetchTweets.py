#!/usr/bin/env python
# encoding: utf-8

import csv
import re
import os.path
import tweepy

#Sanitize Tweets
def sanitize_tweet(tweet):
	clean = re.sub(r"(?:\@|https?\://)\S+", "", tweet) #remove URLS
	clean = clean.replace("&amp;","&")
	clean = clean.replace("&lt;","<")
	clean = clean.replace("&gt;",">")
	clean = clean.replace("’","'")
	return clean
	
def sanitize_tweets(tweets):
	sanitized = []
	for tweet in tweets:
		sanitized.append(sanitize_tweet(tweet))
	return sanitized

#Fetch tweets
#Credit: https://gist.github.com/yanofsky/5436496
def tweets_for_username(username,api):
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