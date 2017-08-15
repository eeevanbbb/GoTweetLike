import sys
import time
import argparse

import tweepy

from Stream import TweetStreamListener
from RequestParser import RequestParser
from TwitterAPI import TwitterAPI
from TweetData import TweetData
from Generate import Generate
from Blacklist import Blacklist

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

class Bot(object):
    screen_name_to_track = '@GoTweetLike'

    def __init__(self, debug=False):
        self.debug = debug

    def start_listening(self):
        request_parser = RequestParser()
        twitter_api = TwitterAPI(debug=self.debug)
        tweet_data = TweetData(twitter_api)
        generator = Generate()
        blacklist = Blacklist()
        stream_listener = TweetStreamListener(request_parser, twitter_api, tweet_data, generator, blacklist, self.restart)
        stream = tweepy.Stream(auth=twitter_api.api.auth, listener=stream_listener)

        try:
            print 'Starting stream...'
            stream.filter(track=[self.screen_name_to_track])
        except AttributeError as e: # ignore error in Tweepy library (see here: https://github.com/tweepy/tweepy/issues/576)
            print "Caught AttributeError (%s)" % e.message
            self.restart()

    def restart(self):
        print 'Restarting GoTweetLike...'
        self.start_listening()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start GoTweetLike.')
    parser.add_argument('--debug', dest='debug', action='store_const', const=True, default=False, help='Start the bot in DEBUG mode.')
    args = parser.parse_args()

    print 'Starting GoTweetLike...'
    bot = Bot(debug=args.debug)
    bot.start_listening()

