#!/usr/bin/env python
# encoding: utf-8

import re
from random import randint

control_string = "***///END///***"

#Analysis and Generation
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
	
def generate_tweet_with_max_char_length_and_seed(char_length,seed,tweets):
	string = seed
	should_continue = True
	last_word = seed
	next_word = get_next_word(last_word,tweets)
	while len(string) + len(next_word) + 1 <= char_length and should_continue:
		if next_word != "":
			string += " "
			string += next_word
			last_word = next_word
		else:
			should_continue = False
	return string
	
def generate_tweet_with_max_char_length(char_length,tweets):
	seed = choice_from_weighted_dict(get_starting_word_histagram(tweets))
	return generate_tweet_with_max_char_length_and_seed(chat_length,seed,tweets)