# @GoTweetLike
A twitter bot that tweets like people! https://twitter.com/GoTweetLike

## Requirements

* `python 2.7`
* TwitterBot credentials

## Installation

`pip install -r requirements.txt`

## Usage (Run the server)

```
usage: Main.py [-h] [--debug]

Start GoTweetLike.

optional arguments:
  -h, --help  show this help message and exit
  --debug     Start the bot in DEBUG mode.
```

## Usage (Use the bot)

* @GoTweetLike @Username   ---   Bot will reply with a tweet in the style of that user
* @GoTweetLike @AnyUsername update   ---   The bot will force the cache of tweets for that user to update before tweeting
* @GoTweetLike help   ---   Bot will reply with instructions about how to use it
* @GoTweetLike @Username1 @Username2 ... @UsernameN   ---   Bot will reply with a tweet in the combined style of those users

## About

First and foremost, @GoTweetLike is still very much a work in progress!

Second and secondmost, feel free to send a pull request to help me make it better!

@GoTweetLike uses the [markovify](https://github.com/jsvine/markovify) library to create markov models based on a given twitter user's most recent tweets.

## Known issues

* Some encoded strings may appear in the corpus unescaped.

* Unicode not supported.

* Some features from the old version (e.g. linguistic statistics) were scrapped in the rewrite. They are being rebuilt.

* Only up to the most recent 3200 tweets are downloaded per user. This is a limitation of the twitter API. Tweets are cached, however, so that a larger corpus can be built up over time.

## Miscellaneous

My personal twitter is [@EvanSaysHello](https://twitter.com/EvanSaysHello). Follow me if you want to be spammed with lots of tweets testing [@GoTweetLike](https://twitter.com/GoTweetLike) as I continue to develop it.
