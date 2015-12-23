#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
from tweepy import OAuthHandler
import cPickle as pickle
import os
import time
import json
import collections
import functional
from helper import Helper

consumer_key = 'hS9KuselTd4AjDABVEWIMTGzS'
consumer_secret = 'HA2VLDFsN18d5tfV49e1O21OnOaAs2X8CRqMf3o51L2DUcyAgO'
access_token = '3445717934-RNgNJebsfdWKxDqS2RTRuKi5SQID5Z1QMmkuyin'
access_secret = 'jhzdZE2Eo89KCERBszLkmBWEXf3KBdIenVZrJbVDMGvQY'


Tweet = collections.namedtuple('Tweet', ['id', 'author', 'author_id',
                                         'created_at',
                                         'text', 'retweet_count',
                                         'favorite_count', 'entities'])


def fetech_tweets(query):
    def makeTweet(status):
        tweet_id = status.id_str
        author = status.author.screen_name
        author_id = status.author.id_str
        created_at = status.created_at
        text = status.text
        entities = status.entities
        favorite_count = status.favorite_count
        retweet_count = status.retweet_count
        return Tweet(tweet_id, author, author_id, created_at, text,
                     retweet_count, favorite_count, entities)

    print "Start to fetch tweets for query: %s" % query
    path = "%s.pickle" % query
    if os.path.exists(path):
        tweets = pickle.load(open(path, "rb"))
        print "load tweets stored in the storage, # of tweets: %d"\
            % len(tweets)
        return tweets

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    param = {
        "q": query,
        "rpp": 100
    }

    tweets = []
    cursor = tweepy.Cursor(api.search, **param).items()
    while True:
        try:
            status = cursor.next()
            tweets.append(makeTweet(status))
        except tweepy.TweepError:
            print("Reach rate limit, sleep for 15 minutes...")
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break
    print "%d tweets had been fetched." % len(tweets)
    tweets = sorted(tweets, key=lambda t: t.created_at)
    pickle.dump(tweets, open(path, "wb"))
    return tweets


def dump_timeline(tweets, title="Timeline"):
    def makeEvent(d):
        return {"year": d.year, "month": d.month,
                "day": d.day, "hour": d.hour,
                "hour": d.hour, "minute": d.minute, "second": d.second}

    def makeText(headline="Headline", text=""):
        return {"headline": headline, "text": text}

    def toEvents(tweet):
        return {
                "start_date": makeEvent(tweet.created_at),
                "text": makeText(tweet.id, tweet.text),
                "author": {"author": tweet.author, "author_id": tweet.author_id}
               }

    events = map(toEvents, tweets)

    title_obj = {"text": makeText("Timeline", "")}

    output = {"title": title_obj, "events": events}
    json.dump(output, open("html/data.json", "w"))


def preprocess(tweets):
    """TODO: Docstring for preprocess.
    1. remove RT, mentioning, hashtags
    2. run clustering, find the tweet cluster, and the important tweets
        1. time
        2. favorite_count
        3. retweet_count
    3. return the important tweets
    :tweets: TODO
    :returns: TODO

    """

    tweets_seq = functional.seq(tweets)
    tokenized_tweets = tweets_seq.map(lambda t: Helper.tokenize(t.text))
    clear_text = tokenized_tweets.map(lambda t: Helper.clearText(t))
    tfidfs = Helper.tfidf(clear_text)

    return tweets


def main():
    tweets = fetech_tweets("taiwan%20election")
    tweets = preprocess(tweets)

    dump_timeline(tweets)
    print tweets[0]


if __name__ == "__main__":
    main()
