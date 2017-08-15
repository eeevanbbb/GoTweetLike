import os
import csv
import time
import HTMLParser

class TweetData(object):
    time_between_updates = 60 * 60 * 24 #A day (in seconds)
    tweets_folder_name = 'tweets'
    tweets_per_batch = 200
    debug_tweets_filepath = 'tweets/~DebugTweets_DebugTweets~.csv'

    def __init__(self, api):
        self.api = api

    # https://gist.github.com/yanofsky/5436496
    def fetch_tweets(self, screen_name, newest=None):
        all_tweets = []

        new_tweets = self.api.user_timeline(screen_name, self.tweets_per_batch, since_id=newest)

        if len(new_tweets) == 0:
            return all_tweets

        all_tweets.extend(new_tweets)

        oldest = all_tweets[-1].id - 1

        while len(new_tweets) > 0:
            print 'Getting tweets before ' + str(oldest)

            new_tweets = self.api.user_timeline(screen_name, self.tweets_per_batch, max_id=oldest, since_id=newest)

            all_tweets.extend(new_tweets)

            oldest = all_tweets[-1].id - 1

            print "...%s tweets downloaded so far" % (len(all_tweets))

        return [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in all_tweets]            

    def update_tweets_if_necessary(self, screen_name, force=False):
        if not self.api.debug:
            filepath = self.tweets_folder_name + '/%s.csv' % screen_name

            if not os.path.isfile(filepath):
                tweets = self.fetch_tweets(screen_name)

                try:
                    with open(filepath, 'w') as tweets_file:
                        writer = csv.writer(tweets_file)
                        writer.writerows(tweets)
                except IOError:
                    print 'Could not open tweets file: ' + filepath
            else:
                last_modified = os.path.getmtime(filepath)

                if force or last_modified + self.time_between_updates < time.time():
                    print 'Updating tweets for ' + screen_name

                    try:
                        with open(filepath, 'ra') as tweets_file:
                            reader = csv.reader(tweets_file)

                            newest_tweet = next(reader, None)
                            if newest_tweet != None:
                                newest_tweet_id = newest_tweet[0]

                                new_tweets = self.fetch_tweets(screen_name, long(newest_tweet_id))

                                tweets_file.seek(0)

                                writer = cvs.writer(tweets_file)
                                writer.writerows(new_tweets)
                            else:
                                print 'Tweets file contains no tweets: ' + filepath
                    except IOError:
                        print 'Could not open tweets file: ' + filepath

    def tweets(self, screen_name):
        filepath = 'tweets/%s.csv' % screen_name
        if self.api.debug:
            filepath = self.debug_tweets_filepath

        try:
            with open(filepath, 'r') as tweets_file:
                tweets = []

                reader = csv.reader(tweets_file)
                for row in reader:
                    tweet_text = row[2]
                    tweets.append(self.sanitize(tweet_text))

                return tweets
        except IOError:
            print 'Could not open tweets file: ' + filepath

            return []

    def sanitize(self, tweet):
        return tweet # TODO: what needs to be done here?
