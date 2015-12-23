#!/usr/bin/env python
# encoding: utf-8
import re
import functional
from nltk.corpus import stopwords
import twokenize


class Helper(object):
    """docstring for Helper"""

    @classmethod
    def clearText(self, tokens):
        """@todo: Docstring for clearText.
        Remove RT, mentioning, hashtags, punctuations, stopwords, punctuations,
        urls

        :tokens: tokens to be processed
        :returns: clean tokens

        """
        stops = stopwords.words('english')
        rt_pattern = re.compile(r"RT")
        mention_pattern = re.compile(r"@[\d\w_]+")
        hashtag_pattern = re.compile(r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)")
        url_pattern = re.compile(r"http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]" +
                                 "|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+")

        return functional.seq(tokens)\
            .filter(not rt_pattern.match(_))\
            .filter(not mention_pattern.match(_))\
            .filter(not hashtag_pattern.match(_))\
            .filter(not url_pattern.match(_))\
            .filter(_ not in stops)\
            .to_list()

    @classmethod
    def tokeninze(text):
        return twokenize.tokeninze(text)

    @classmethod
    def tfidf(tokens_list):
        tfidfVectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,3),
                                          max_features=100, stop_words='english')
        corpus = (" ".join(tokens)] for tokens in tokens_list)

        tfidf = tfidfVectorizer.fit_transform(corpus)
        return tfidf
