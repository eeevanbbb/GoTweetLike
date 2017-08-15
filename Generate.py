import markovify

class Generate(object):
    tweet_length = 140

    def generate_text_model(self, tweets):
        return markovify.Text("\n".join(tweets), state_size=1)

    def generate_short_sentence(self, tweets, length):
        return self.generate_text_model(tweets).make_short_sentence(length)

    def generate_reply(self, text, reply_to):
        return '@' + reply_to + ' ' + text

    def available_length(self, reply_to):
        return self.tweet_length - len(self.generate_reply('', reply_to))

    def generate_standard_tweet(self, tweets, reply_to):
        return self.generate_reply(self.generate_short_sentence(tweets, self.available_length(reply_to)), reply_to)

    def generate_combined_tweet(self, tweet_sets, reply_to):
        models = [self.generate_text_model(tweets) for tweets in tweet_sets]
        weights = [1.0 for tweets in tweet_sets]
        combined_model = markovify.combine(models, weights)
        return self.generate_reply(combined_model.make_short_sentence(self.available_length(reply_to)), reply_to)