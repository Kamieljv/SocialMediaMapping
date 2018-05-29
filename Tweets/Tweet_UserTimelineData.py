"""
Modified on Tue 29 May 2018
@author: Kamieljv (GitHub)

Tweet_UserTimelineData.py:
    scrapes user timelines for tweets
    extracts coordinates (if any) and writes to csv
"""

from twitter import *
import oauthlib
import json
import csv
import time

# add authentification details
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

userfile = '' #file with unique usernames, all on new lines
outfile = '' #csv file to write the coordinates to, preferably ends with '_' (because file nr is added)
twitter = Twitter(auth = OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

#---------HELPER FUNCTIONS--------------------
def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=False)))
#-------------------------------------------------

users = []
with open(userfile) as file:
    for user in file:
        user = user.replace('\n','')
        users.append(user)
l_us = len(users)
print(l_us, 'total users')
start = 0 #allows the programme to start at a different user index
j=0
tot_locs = 0 #keeps track of how many locations were found in current run
sender_locs = []
for i,user in enumerate(users[start:]):
    if i%100==0: #write locs of 100 users per file
        if sender_locs:
            nr = '%04d' %(j+start/100)
            with open(outfile+nr+'.csv', 'w', newline='') as file: #write csv file with coordinates (lon, lat)
                csvwriter = csv.writer(file, delimiter=',')
                for line in sender_locs:
                    csvwriter.writerow([line[0], line[1]])
        j+=1
        sender_locs = []
    results = []
    #make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        new_tweets = twitter.statuses.user_timeline(screen_name = user, count=200)
        results.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = results[-1]['id'] - 1
        while len(new_tweets) > 0:
            #all subsequent requests use the max_id param to prevent duplicates
            new_tweets = twitter.statuses.user_timeline(screen_name = user, count=200, max_id=oldest)

            #save most recent tweets
            results.extend(new_tweets)

            #update the id of the oldest tweet less one
            oldest = results[-1]['id'] - 1

        sender_locs_user = []
        for tweet in results:
            try:
                coord = tweet['coordinates'] #try if there is a coordinate attached to the tweet
            except Exception:
                pass

            if coord:
                longlat = coord['coordinates'] #list of LONG-LAT coordinates of tweet
                sender_locs_user.append(longlat)
        tot_locs += len(sender_locs_user)
        sender_locs.extend(sender_locs_user)
        print("{}   /   {}  User: {}    Tweets: {}  Locations: {}   Total Locs: {}".format(i+start, len(users), repr(user), len(results), len(sender_locs_user), tot_locs))

    except Exception as e:
        print("{}   User: {}    FAILED".format(i+start, repr(user))) #Some requests fail, for unknown reasons
        time.sleep(1)

#write any leftover locations in sender_locs to a csv
nr = '%04d' %(j+start/100)
with open(outfile+nr+'.csv', 'w', newline='') as file:
    csvwriter = csv.writer(file, delimiter=',')
    for line in sender_locs:
        csvwriter.writerow([line[0], line[1]])