#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Tweet(object):
    """docstring for Tweet"""

    def __init__(self, id, author, author_id, created_at, text, entities,
                 favorite_count, retweet_count):
        self.id = id
        self.author = author
        self.author_id = author_id
        self.created_at = created_at
        self.text = text
        self.entities = entities
        self.favorite_count = favorite_count
        self.retweet_count = retweet_count

    @classmethod
    def generate(cls, status):

        tweet_id = status.id_str
        author = status.author.screen_name
        author_id = status.author.id_str
        created_at = status.created_at
        text = status.text
        entities = status.entities
        favorite_count = status.favorite_count
        retweet_count = status.retweet_count
        tweet = Tweet(tweet_id, author, author_id, created_at, text,
                      entities, favorite_count, retweet_count)
        return tweet
