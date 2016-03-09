# @GoTweetLike
A twitter bot that tweets like people! https://twitter.com/gotweetlike

## Usage

* @GoTweetLike @AnyUsername   ---   Bot will reply with a tweet in the style of that user
* @GoTweetLike @AnyUsername about AnyTopic   ---   If that user has tweeted about that topic before, bot will reply with a tweet about that topic
* @GoTweetLike @AnyUsername stats   ---   Bot will reply with some basic stats about that user's tweets

## About

First and foremost, @GoTweetLike is still very much a work in progress!

Second and secondmost, feel free to send a pull request to help me make it better!

@GoTweetLike works by building a frequency table from a given user's last 3,200 tweets (the maximum amount Twitter's API will allow the bot to fetch), then building a new random sentence based on how likely some words are to follow other words. It has no knowledge of language structure or syntax.

## Known issues

* Right now, @GoTweetLike's analyses are case-sensitive. This can be good, for instance, to give context hints about when words are capitalized (i.e. the beginning of a sentence), but this can also be bad by fracturing the table when capitalization is arbitrary.

* Right now, @GoTweetLike's "about" feature simply starts the new tweet with the given topic. There are obviously better ways to do this, because often the topic of a tweet is not its first word.

* Right now, @GoTweetLike only looks at the one previous word when reasoning about the next word. It could be smarter!

Notice how these issues all begin with "Right now." This is because @GoTweetLike is being actively developed. Feel free to help! Send a pull request! Send me an email! Send your hacker friend an email!

## Miscelanious

My personal twitter is @EvanSaysHello. Follow me if you want to be spammed with lots of tweets testing @GoTweetLike as I continue to develop it.
