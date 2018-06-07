#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modified on Tue 29 May 2018
@author: Kamieljv (GitHub)
Source: derived from foost (GitHub): https://github.com/foost/PublicResearchPortfolio/blob/master/Code/twitterdatacollection_streamingAPI.py

Tweet_Processing.py:
    load a txt file with JSON-formatted tweets (from Tweet_Collection.py)
    extract coordinates, timestamps, usernames and tweet text
    write this to a csv file
"""

import twitter
import json
import time

# set query parameters
TRACK = '' #Comma-separated list of terms
LOCATIONS = '' #bounding box (xmin, ymin, xmax, ymax) with x=>longitude, y=>latitude

# set path to output files
OUTPUT_PATH = ''

# add authentification details
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

def oauth_login():
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


def save_json(filename, data):
    with open('{}{}.txt'.format(OUTPUT_PATH, filename),'a') as f:
        f.write(json.dumps(data, ensure_ascii=False).encode('utf-8')+'\n')


def main():
    twitter_api = oauth_login()
    filename = "" + time.strftime("%Y%m%d-%H%M%S")
    twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
    twitter_tweets = twitter_stream.statuses.filter(track=TRACK,
                                                   locations=LOCATIONS)
    for tweet in twitter_tweets:
        save_json(filename, tweet)

if __name__=="__main__":
    main()