import tweepy

from TwitterCredentials import Credentials

class TwitterAPI(object):
    def __init__(self, debug=False):
        self.debug = debug

        self.credentials = Credentials()

        self.initialize_api()

    def initialize_api(self):
        auth = tweepy.OAuthHandler(self.credentials.consumer_key(), self.credentials.consumer_secret())
        auth.set_access_token(self.credentials.access_key(), self.credentials.access_secret())
        self.api = tweepy.API(auth)

    def tweet(self, status, in_reply_to_status_id=None):
        if not self.debug:
            self.api.update_status(status=status,
                                    in_reply_to_status_id=in_reply_to_status_id)
        print('Tweeting: "' + status + '" in reply to: ' + str(in_reply_to_status_id))

    def user_timeline(self, screen_name, count, max_id=None, since_id=None):
        if not self.debug:
            return self.api.user_timeline(screen_name=screen_name, 
                                            count=count,
                                            max_id=max_id,
                                            since_id=since_id)
        else:
            return None

    def follow(self, screen_name):
        if not self.debug:
            self.api.create_friendship(screen_name)
        print 'Following ' + screen_name