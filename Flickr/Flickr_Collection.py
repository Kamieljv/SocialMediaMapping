#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modified on Wed 06 Jun 2018
@author: Kamieljv (GitHub)
Source: derived from foost (GitHub): https://github.com/foost/PublicResearchPortfolio/blob/master/Code/flickrDataCollection_searchAPI.py
Flickr_Collection.py:
    access FlickrAPI
    write metadata as in text file

code is not optimized for performance or brevity,
aims instead for readability and ease of understanding
"""

import flickrapi
import datetime
import time
import sys
import os

#
# declare global USER variables
#

# output path (end with double backslash!) and file name trunk
PATH = ''
FILE_OUT_TRUNK = ''

# api_key
API_KEY = '808d84249c787469c00bbf620e9e55f3'
API_SECRET = '61af9243816414e1'

# define search query keywords, dates and location;
# radius unit is km, default is 5
# bounding box min_lon, min_lat, max_lon, max_lat
SEARCH_QUERY = ''
START_DATE = '' #format: YYYY-MM-DD
END_DATE = '' #format: YYYY-MM-DD
LAT = ''
LON = ''
RADIUS = ''
BBOX = '' #bounding box, xmin, ymin, xmax, ymax

today = time.strftime("%Y%m%d-%H%M%S")

# define search extras to be retrieved
SEARCH_EXTRAS = 'date_taken, date_upload, description, owner_name, geo, tags'

# flow control for this script
# tags_raw = 'yes' if raw tags should be retrieved; however, this makes
# execution much slower; since queries do not return all photos all the time
# (Flickr API bug), queries with large results sets might not want to use this
# count_only = 'yes' to execute only initial query returning number of photos
TAGS_RAW = 'yes'
COUNT_ONLY = 'no'

# list of values to be written to file
# owner_subelements_list currently not used
PHOTO_ATTR_LIST = ['id', 'title', 'owner', 'ownername', 'datetaken',
                   'dateupload', 'latitude', 'longitude', 'accuracy', 'tags']
PHOTO_SUBELEM_LIST = ['description']
#owner_subelements_list = ['realname', 'location']

# function to replace all problematic characters in the retrieved text
def replace_chars(text):
        text = text.replace('\r',' ')\
                    .replace('\n', ' ')\
                    .replace('\t', ' ')\
                    .replace(',', ' ')\
                    .replace("'", " ")\
                    .replace('"', ' ')\
                    #.replace('\\','/') #this one might clash with unicode
        return text

# function to search if bounding box is given
def search_latlonrad(flickr,min_taken_date,max_taken_date,page):
    search_results = flickr.photos_search(
                text = SEARCH_QUERY,
                min_taken_date = min_taken_date,
                max_taken_date = max_taken_date,
                extras = SEARCH_EXTRAS,
                lat = LAT,
                lon = LON,
                radius = RADIUS,
                page = page)
    return search_results

# function to search if lat/lon and radius are given
def search_bbox(flickr,min_taken_date,max_taken_date,page):
    search_results = flickr.photos_search(
                text = SEARCH_QUERY,
                min_taken_date = min_taken_date,
                max_taken_date = max_taken_date,
                extras = SEARCH_EXTRAS,
                bbox = BBOX,
                page = page)
    return search_results

def main():
    # create flickr instance
    flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET)
    flickr.authenticate_via_browser(perms='read')

    # get total number of search results
    # cannot use lat/lon/radius with an empty bbox, therefore IF-THEN
    if BBOX == '':
        search_results = search_latlonrad(flickr,START_DATE,END_DATE,0)
    else:
        search_results = search_bbox(flickr,START_DATE,END_DATE,0)

    photos_query_total = search_results.find('photos').get('total')
    print("Total number of photos according to API: " + str(photos_query_total))

    if COUNT_ONLY == 'yes':
        sys.exit("exiting...")

    # create new directory if necessary and write meta data to info file
    new_dir = "%s%s\\" %(PATH, FILE_OUT_TRUNK)
    if not os.path.exists(new_dir):
        try:
            os.makedirs(new_dir)
        except:
            print("Could not create new directory!")
            sys.exit()

    # info file on search query
    f_info=open("Flick_"+today+"_info.txt", 'w')
    f_info.write('query_time, query, start_date, end_date, lat, lon, bbox,'\
                 ' extras, raw_tags, number_of_photos,'\
                 ' counted, ignored, processed\n')

    header = ""
    for column in PHOTO_ATTR_LIST:
        header += column + '\t'
    header += 'tags_raw\t'
    for column in PHOTO_SUBELEM_LIST:
        header += column + '\t'
    #for column in owner_subelements_list:
    #    header += column + '\t'
    header = header.rstrip('\t')

    # start actual retrieval of data
    # first convert query dates to integer
    start_iter = datetime.datetime.strptime(START_DATE,"%Y-%m-%d").toordinal()
    end_iter = datetime.datetime.strptime(END_DATE,"%Y-%m-%d").toordinal()

    # initiate counters and list to filter out duplicates
    counter = 0
    ignored = 0
    processed = 0
    fid_list = []
    j=0
    # end_iter +1 needed to get last day
    for i in range(start_iter, end_iter+1):

        print("day ",str(i))
        query_date = datetime.date.fromordinal(i)

        # open output file
        if i==start_iter or (start_iter-i)%30==0: #for first iteration, create output file
            if i!=start_iter:
                f_results.close()
                j+=1
            nr = '%04d' %j
            f_results = open("Flick_" +today+"_"+nr+".txt", 'w')
            print(header+"\n")
            f_results.write(header + "\n")

        # using single days +-1 retrieves more reliable results
        min_query_date = datetime.date.fromordinal(i-1)
        max_query_date = datetime.date.fromordinal(i+1)
        if BBOX == '':
            search_results_daily = search_latlonrad(flickr,min_query_date,max_query_date,0)
        else:
            search_results_daily = search_bbox(flickr,min_query_date,max_query_date,0)

        # to avoid rate limits, wait one second after api call
        time.sleep(1)

        # iterate over pages; it is possible to specify number of photos per
        # page, but it does not change maximum number of photos per query
        # (always 4000); therefore best to leave it at default (100 photos per page)
        print("page ")
        for i in range (int(search_results_daily.find('photos').get('pages'))+2):
            print(str(i))
            # try statement needed because there occasional API errors
            try:
                if BBOX == '':
                    search_results_daily_paginated = search_latlonrad(
                            flickr,min_query_date,max_query_date, i)
                else:
                    search_results_daily_paginated = search_bbox(
                            flickr,min_query_date,max_query_date, i)

                # to avoid rate limits, wait one second after api call
                time.sleep(1)

                # Iterate over photos in page
                photo_iter = search_results_daily_paginated.getiterator('photo')
                for photo in photo_iter:
                    counter += 1
                    try:
                        fid = photo.get('id')
                        # check whether photo has already been processed
                        if fid in fid_list:
                            ignored += 1
                            break
                        fid_list.append(fid)
                        out_row = fid + '\t'

                        for attribute in PHOTO_ATTR_LIST[1:]:
                            value = photo.get(attribute)
                            # convert datetaken into posix timestamp
                            if attribute == 'datetaken':
                                value = time.mktime(datetime.datetime.strptime(
                                        value, "%Y-%m-%d %H:%M:%S").timetuple())
                                out_row += str(int(value)) + '\t'
                            else:
                                if value is None:
                                    value = 'NODATA'
                                value = replace_chars(value)
                                out_row += value + '\t'

                        if TAGS_RAW == 'yes':
                            raw_tags = ''
                            tags = flickr.tags_getlistphoto(photo_id = fid)
                            # no wait possible here, otherwise takes too long
                            tag_iter = tags.getiterator('tag')
                            if tag_iter is None:
                                raw_tags = 'NODATA'
                            for tag in tag_iter:
                                raw_tag = tag.get('raw')
                                raw_tag = replace_chars(raw_tag)
                                raw_tags += raw_tag + "~"
                            raw_tags = raw_tags.rstrip('~')
                        else:
                            raw_tags = "NOTQUERIED"
                        out_row += raw_tags + '\t'

                        for photo_subelement in PHOTO_SUBELEM_LIST:
                            value = photo.find(photo_subelement).text
                            if value is None:
                                value = 'NODATA'
                            else:
                                value = replace_chars(value)
                            out_row += value

                        f_results.write(out_row + '\n')
                        print(out_row, 'out')
                        processed += 1

                    except Exception as e:
                        print("Problem with photo!", sys.exc_info()[0], str(e))

            except Exception as e:
                 print("Problem with search page!", sys.exc_info()[0], str(e))

        print("\n",query_date, photos_query_total, counter, ignored, processed)
    f_results.close()

    f_info.write('{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                 datetime.date.today(),SEARCH_QUERY,START_DATE,
                 END_DATE,LAT,LON,BBOX,SEARCH_EXTRAS,TAGS_RAW,
                 photos_query_total, counter, ignored, processed))
    f_info.close()

if __name__=="__main__":
    main()