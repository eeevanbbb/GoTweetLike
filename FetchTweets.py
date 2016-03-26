#!/usr/bin/env python
# encoding: utf-8

import csv
import re
import os.path
import tweepy
import time

#Constants
TIME_BETWEEN_UPDATES = 60 * 60 * 24 #A day (in seconds)

#Sanitize Tweets
def sanitize_tweet(tweet):
	clean = re.sub(r"(?:\@|https?\://)\S+", "", tweet) #remove URLS
	clean = clean.replace("&amp;","&")
	clean = clean.replace("&lt;","<")
	clean = clean.replace("&gt;",">")
	clean = clean.replace("’","'")
	#Remove initial whitespace (generally from the first word(s) being scrubbed)
	if len(clean) >= 1 and clean[0] == " ":
		clean = clean[1:]
	return clean
	
def sanitize_tweets(tweets):
	sanitized = []
	for tweet in tweets:
		sanitized.append(sanitize_tweet(tweet))
	return sanitized

#Credit: https://gist.github.com/yanofsky/5436496
def get_tweets_internal(username,api,newest):
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	

	#make initial request for most recent tweets (200 is the maximum allowed count)
	if newest is None:
		new_tweets = api.user_timeline(screen_name = username,count=200)
	else:
		new_tweets = api.user_timeline(screen_name = username,count=200,since_id=newest)

	if len(new_tweets) == 0:
		return alltweets

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
	
		#all subsiquent requests use the max_id param to prevent duplicates
		if newest is None:
			new_tweets = api.user_timeline(screen_name = username,count=200,max_id=oldest)
		else:
			new_tweets = api.user_timeline(screen_name = username,count=200,max_id=oldest,since_id=newest)
	
		#save most recent tweets
		alltweets.extend(new_tweets)
	
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
	
		print "...%s tweets downloaded so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	return outtweets

#Fetch tweets
def tweets_for_username(username,api,update):
	filepath = 'tweets/%s_tweets.csv' % username
	#If the file does not exist, write one with most recent tweets
	if not os.path.isfile(filepath):
		outtweets = get_tweets_internal(username,api,None)
	
		#write the csv	
		with open('tweets/%s_tweets.csv' % username, 'wb') as f:
			writer = csv.writer(f)
			#writer.writerow(["id","created_at","text"])
			writer.writerows(outtweets)
	
	#If the file exists and has not been modified for X time, fetch new tweets and append
	else:
		mtime = os.path.getmtime(filepath)
		if update is True or mtime + TIME_BETWEEN_UPDATES < time.time():
			print "Updating Tweets for " + username
    		#Get id of most recent tweet we have
			with open('tweets/%s_tweets.csv' % username, 'r+') as f:
				reader = csv.reader(f)
				for row in reader:
					tweetid = row[0]
					break
				
			#Get new tweets, write them first, then rewrite the old data
			with open('tweets/%s_tweets.csv' % username, 'r+') as f:
				outtweets = get_tweets_internal(username,api,long(tweetid))
				old_file = f.read()
				f.seek(0)
				writer = csv.writer(f)
				writer.writerows(outtweets)
				f.write(old_file)
	
	#Read tweets from the csv
	tweets = []
	with open('tweets/%s_tweets.csv' % username, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			tweet = row[2]
			tweets.append(tweet)
			
	tweets = sanitize_tweets(tweets)	
	return tweets