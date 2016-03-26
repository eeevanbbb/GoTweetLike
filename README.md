# @GoTweetLike
A twitter bot that tweets like people! https://twitter.com/GoTweetLike

## Usage

* @GoTweetLike @AnyUsername   ---   Bot will reply with a tweet in the style of that user
* @GoTweetLike @AnyUsername about AnyTopic   ---   If that user has tweeted about that topic before, bot will reply with a tweet about that topic
* @GoTweetLike @AnyUsername stats   ---   Bot will reply with some basic stats about that user's tweets
* @GoTweetLike @AnyUsername advanced stats   ---   Bot will reply with more advanced stats about that user's tweets
* @GoTweetLike @AnyUsername update   ---   If the bot has cached tweets for the user, it will update this cache before tweeting

## About

First and foremost, @GoTweetLike is still very much a work in progress!

Second and secondmost, feel free to send a pull request to help me make it better!

@GoTweetLike works by building a frequency table from a given user's last 3,200 tweets (the maximum amount Twitter's API will allow the bot to fetch), then building a new random sentence based on how likely some words are to follow other words. It has no knowledge of language structure or syntax.

Tweets are cached once downloaded, and new tweets are added at most daily (when the user is requested) or whenever an update is forced (see Usage above)

## Known issues

* Right now, @GoTweetLike's analyses are case-sensitive. This can be good, for instance, to give context hints about when words are capitalized (i.e. the beginning of a sentence), but this can also be bad by fracturing the table when capitalization is arbitrary.

* Right now, @GoTweetLike only looks at the one previous word when reasoning about the next word. It could be smarter!

* Right now, @GoTweetLike tries to end tweets where the user would, but there is a hard limit at 140 characters (minus overhead).

Notice how these issues all begin with "Right now." This is because @GoTweetLike is being actively developed. Feel free to help! Send a pull request! Send me an email! Send your hacker friend an email!

## Miscellanious

My personal twitter is @EvanSaysHello. Follow me if you want to be spammed with lots of tweets testing @GoTweetLike as I continue to develop it.
