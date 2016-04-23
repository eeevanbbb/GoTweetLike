#!/usr/bin/env python
# encoding: utf-8

def get_tweet_type(tweet):
	words = tweet.split()
	if len(words) < 2:
		return "Invalid"
	elif words[0].lower() == "@gotweetlike" and words[1][0] == "@":
		scannableWords = words[2:]
		scannableString = " ".join(scannableWords).lower()
		if len(words) >= 3 and words[2].lower() == "stats":
			return "Stats"
		elif len(words) >= 3 and words[2].lower() == "update":
			return "Update"
		elif len(words) == 4 and words[2].lower() == "about":
			return "Topic: " + words[3]
		elif len(words) >= 4 and (words[2].lower() == "advanced" or words[2].lower() == "more") and words[3].lower() == "stats":
			return "AdvancedStats"
		elif len(words) >= 4 and words[2].lower() == "longest" and (words[3].lower() == "word" or words[3].lower() == "words"):
			return "LongestWord"
		#More lenient scanning
		elif "longest word" in scannableString or "longest words" in scannableString:
			return "LongestWord"
		elif "advanced stats" in scannableString or "more stats" in scannableString:
			return "AdvancedStats"
		elif "stats" in scannableString:
			return "Stats"
		elif "update" in scannableString:
			return "Update"
		#Default to standard
		else:
			return "Standard"
	
	return "Invalid"