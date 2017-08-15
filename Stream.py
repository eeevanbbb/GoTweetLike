import tweepy
import threading

class TweetStreamListener(tweepy.StreamListener):
    my_user_id = "706605179911602176"
    my_screen_name = "@GoTweetLike"

    def __init__(self, request_parser, twitter_api, tweet_data, generator, blacklist, restart):
        tweepy.StreamListener.__init__(self)

        self.request_parser = request_parser
        self.twitter_api = twitter_api
        self.tweet_data = tweet_data
        self.generator = generator
        self.blacklist = blacklist
        self.restart = restart

        self.processed_requests = []

    def on_status(self, status):
        new_thread = threading.Thread(target=self.process_status_worker, args=(status,))
        new_thread.start()

    def process_status_worker(self, status):
        if status.id not in self.processed_requests:
            self.processed_requests.append(status.id)

            if status.user.id_str != self.my_user_id and not status.is_quote_status and not status.retweeted:
                print 'Processing tweet: ' + status.text

                if status.user.screen_name in self.blacklist.blacklist:
                    print 'User is on blacklist: ' + status.user.screen_name
                    return

                parsed = self.request_parser.parse_request(status.text)

                reply_tweet = None
                screen_name_to_tweet_like = None
                follow = []

                print 'Tweet is of type: ' + parsed["type"]

                if parsed["type"] == "help":
                    reply_tweet = self.generator.generate_reply(parsed["message"], status.user.screen_name)
                elif parsed["type"] == "invalid":
                    if status.in_reply_to_status_id_str is None:
                        reply_tweet = self.generator.generate_reply(parsed["message"], status.user.screen_name)
                elif parsed["type"] in ["standard", "update"]:
                    screen_name_to_tweet_like = parsed["screen_name"]
                    follow.append(screen_name_to_tweet_like)
                    
                    self.tweet_data.update_tweets_if_necessary(screen_name_to_tweet_like, force=parsed["type"] == "update") # blocking
                    tweets = self.tweet_data.tweets(screen_name_to_tweet_like)

                    reply_tweet = self.generator.generate_standard_tweet(tweets, status.user.screen_name)
                elif parsed["type"] == "combined":
                    screen_names_to_tweet_like = parsed["screen_names"]
                    follow = screen_names_to_tweet_like
                    tweet_sets = []
                    for screen_name in screen_names_to_tweet_like:
                        self.tweet_data.update_tweets_if_necessary(screen_name) # blocking
                        tweet_sets.append(self.tweet_data.tweets(screen_name))
                    reply_tweet = self.generator.generate_combined_tweet(tweet_sets, status.user.screen_name)


                if reply_tweet != None:
                    self.twitter_api.tweet(reply_tweet, in_reply_to_status_id=status.id)

                self.twitter_api.follow(status.user.screen_name)
                for screen_name in follow:
                    if screen_name.lower() != self.my_screen_name.lower():
                        self.twitter_api.follow(screen_name[1:])

    def on_error(self, status_code):
        print "Encountered stream error: %d" % status_code
        if status_code == 420:
            return False
#           print "sleeping..."
#           time.sleep(60*15)
#           start_server()
        else:
            restart()

