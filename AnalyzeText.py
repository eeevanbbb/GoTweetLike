#!/usr/bin/env python
# encoding: utf-8

import re
from random import randint
import operator

control_string = "***///END///***"
begin_control_string = "***///BEGIN///***"
regex_pattern = "(#*\w[\w']*\w\.?|\w\.?|\&)" #Allow for hashtags, contractions, periods, and ampersands

#Analysis and Generation
def get_successor_histagram(tweets):
	dict = {}
	for tweet in tweets:
		rgx = re.compile(regex_pattern)
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
	
def get_predecessor_histagram(tweets):
	dict = {}
	for tweet in tweets:
		rgx = re.compile(regex_pattern)
		words = rgx.findall(tweet)
		for i in range(1,len(words)+1):
			word = words[len(words)-i]
			previous_word = begin_control_string
			if i < len(words):
				previous_word = words[len(words)-(i+1)]
			if word != "" and previous_word != "":
				if word not in dict:
					dict[word] = {}
				predecessor_dict = dict[word]
				if previous_word in predecessor_dict:
					predecessor_dict[previous_word] += 1
				else:
					predecessor_dict[previous_word] = 1
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
	
def generate_tweet_with_max_char_length(char_length,tweets):
	should_continue = True
	current_word = choice_from_weighted_dict(get_starting_word_histagram(tweets))
	next_word = get_next_word(current_word,tweets)
	string = current_word
	while len(string) + len(next_word) + 1 <= char_length and should_continue:
		if next_word != "":
			string += " "
			string += next_word
			current_word = next_word
			next_word = get_next_word(current_word,tweets)
		else:
			should_continue = False
	return string
	
def get_previous_word(word,tweets):
	predecessor_histagram = get_predecessor_histagram(tweets)
	if word not in predecessor_histagram:
		return ""
	else:
		predecessor_dict = predecessor_histagram[word]
		previous_word = choice_from_weighted_dict(predecessor_dict)
		if previous_word == begin_control_string:
			return ""
		else:
			return previous_word

def generate_tweet_about_topic_with_max_char_length(topic,char_length,tweets):
	#First, go backward
	string = topic
	should_continue = True
	current_word = topic
	previous_word = get_previous_word(current_word,tweets)
	while len(string) + len(previous_word) + 1 <= char_length and should_continue:
		if previous_word != "":
			string = previous_word + " " + string
			current_word = previous_word
			previous_word = get_previous_word(current_word,tweets)
		else:
			should_continue = False
	
	#Then, go forward
	should_continue = True
	current_word = topic
	next_word = get_next_word(current_word,tweets)
	while len(string) + len(next_word) + 1 <= char_length and should_continue:
		if next_word != "":
			string += " "
			string += next_word
			current_word = next_word
			next_word = get_next_word(current_word,tweets)
		else:
			should_continue = False
	
	return string
	

#Stats
def generate_simple_frequency_table(tweets):
	table = {}
	for tweet in tweets:
		rgx = re.compile("(#*\w[\w']*\w\.?|\w\.?)")
		words = rgx.findall(tweet)
		for word in words:
			if word not in table:
				table[word] = 1
			else:
				table[word] += 1
	return table
	
def get_most_frequent_word(table):
	sorted_vals = sorted(table.items(), key=operator.itemgetter(1))
	most_frequent = sorted_vals[-1]
	return most_frequent[0]		

def get_average_number_of_words(tweets):
	total = 0
	for tweet in tweets:
		rgx = re.compile(regex_pattern)
		words = rgx.findall(tweet)
		total += len(words)
	return float(total) / float(len(tweets))

def generate_stats_for_tweets(tweets):
	table = generate_simple_frequency_table(tweets)
	most_frequent_word = get_most_frequent_word(table)
	stats_string = "From %d tweets, the most common word was \"%s\" (%d)." % (len(tweets), most_frequent_word, table[most_frequent_word])
	stats_string += " Average %.1f words per tweet." % get_average_number_of_words(tweets)
	return stats_string


def get_most_common_word_pairing(tweets):
	successor_histagram = get_successor_histagram(tweets)
	most = 0
	most_first_word = ""
	most_second_word = ""
	for first_word in successor_histagram:
		frequency_dict = successor_histagram[first_word]
		for second_word in frequency_dict:
			frequency = frequency_dict[second_word]
			if frequency > most and second_word != control_string:
				most = frequency
				most_first_word = first_word
				most_second_word = second_word
	return "\"" + most_first_word + " " + most_second_word	+ "\" (" + str(most) + ")"
	
def get_average_letters_per_word(tweets):
	letter_count = 0
	word_count = 0
	for tweet in tweets:
		rgx = re.compile(regex_pattern)
		words = rgx.findall(tweet)
		word_count += len(words)
		for word in words:
			letter_count += len(word)
	return float(letter_count) / float(word_count)

	
def generate_advanced_stats_for_tweets(tweets):
	stats_string = "Analyzed %d tweets." % len(tweets)	
	stats_string += " Most common word pairing: %s." % get_most_common_word_pairing(tweets)
	stats_string += " Average %.1f letters per word." % get_average_letters_per_word(tweets)
	return stats_string
