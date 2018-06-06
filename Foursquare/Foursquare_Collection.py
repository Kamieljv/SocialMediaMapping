#! /usr/bin/python
# coding: utf-8

"""
Modified on Wed 06 Jun 2018
@author: Kamieljv (GitHub)
Source: derived from foost (GitHub): https://github.com/foost/PublicResearchPortfolio/blob/master/Code/foursquareDataCollection_searchAPI.py
foursquaredatacollection_searchAPI.py:
    access FoursquareAPI
    write selected metadata in text file

This script is based on the information contained in the Foursquare API and the
Python wrapper documentation.
https://developer.foursquare.com/start/search
https://github.com/mLewisLogic/foursquare
It seems that the most suitable method is search, which does not require user
authentification:
https://developer.foursquare.com/docs/venues/search
Querying the API using a point grid to work around the limitation of 50
returned results per query. However, watch out for rate limits of 5000
userless queries per hour.
example set to Enschede
"""

import foursquare
import csv
import math
import time

#
# declare variables
#

# API keys
CLIENT_ID = ''
CLIENT_SECRET = ''

POINTGRID = '' # path to pointgrid file for input (csv)
RADIUS = float() # radius around which to scan for venues
OUTPUTCSV = '' #output filename
PATH = '' #output filepath
today = time.strftime("%Y%m%d-%H%M%S")

start_point = 0

def main():
    client = foursquare.Foursquare(client_id = CLIENT_ID,
                                   client_secret = CLIENT_SECRET)
    with open('{}{}'.format(PATH, POINTGRID), 'r') as csvin:
        filereader = csv.reader(csvin)
        #next(filereader)
        with open('{}{}'.format(PATH, OUTPUTCSV+today+'.csv'), 'w') as csvout:
            filewriter = csv.writer(csvout)
            fields = ['vid', 'name', 'lat', 'lon', 'category', 'tipCount',
                      'checkinsCount', 'usersCount']
            filewriter.writerow(fields)
            place_ids = []
            pid = 0
            points = 5810
            vcount = 0
            for rowin in filereader:
                if not rowin[0]=='X':
                    print('Progress:    '+str(round(int(pid)/points*100,1))+' % '+'Pid: '+str(pid)+'/ 5809'+' Venues: '+str(vcount))
                    lon = rowin[0]
                    lat = rowin[1]
                    pid = rowin[2]
                    if int(pid) > start_point:
                        try:
                            venues = client.venues.search(params={'ll': '%s, %s' %(lat,lon),
                                                          'intent': 'browse',
                                                          'radius': '%s' %(RADIUS)})
                        except Exception:
                            filewriter.writerow(['Quota_exceeded', pid])
                            return
                        vcount += len(venues['venues'])
                        for venue in venues['venues']:
                            if venue['id'] not in place_ids:
                                name = venue['name']
                                vid = venue['id']
                                lat = venue['location']['lat']
                                lon = venue['location']['lng']
                                tips = venue['stats']['tipCount']
                                checkins = venue['stats']['checkinsCount']
                                users = venue['stats']['usersCount']
                                place_ids.append(vid)
                                try:
                                    category = \
                                        venue['categories'][0]['shortName']
                                except IndexError:
                                    category =''
                                rowout = [vid, name, lat, lon, category, tips,
                                          checkins, users]
                                try:
                                    filewriter.writerow(rowout)
                                except Exception:
                                    pass

if __name__=="__main__":
    main()