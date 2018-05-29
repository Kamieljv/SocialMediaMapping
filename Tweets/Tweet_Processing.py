"""
Modified on Tue 29 May 2018
@author: Kamieljv (GitHub)

Tweet_Processing.py:
    load a txt file with JSON-formatted tweets (from Tweet_Collection.py)
    extract coordinates, timestamps, usernames and tweet text
    write this to a csv file
"""

import json
import csv
import ast

filename = '' #text file containing JSON-format tweets
extension = '.txt'
output_filename = '' #csv file output


with open(filename+extension, 'r', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]

tweets = []

for tweet in data:
    try:
        coord = tweet['coordinates'] #try if there is a coordinates element in the tweet
        longlat = coord['coordinates'] #list of LONG-LAT coordinates of tweet
        try:
            screen_name = tweet['user']['screen_name']
        except Exception:
            screen_name = '######'

        tweets.append([longlat[0], longlat[1], tweet['created_at'], tweet["timestamp_ms"], screen_name, tweet['text']])
    except Exception:
        pass

print(len(tweets), 'tweets in total')


with open(output_filename+'.csv', 'w', newline='', encoding='utf-8') as file:
    csvwriter = csv.writer(file, delimiter=',')
    for line in tweets:
        csvwriter.writerow(line)

