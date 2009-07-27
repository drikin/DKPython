#!/usr/bin/env python
# encoding: utf-8
"""
twitter_test.py

Created by Kohichi Aoki on 2009-07-26.
Copyright (c) 2009 drikin.com. All rights reserved.
"""

import sys
import os
import datetime
import codecs
import twitter
from dateutil import zoneinfo, tz

TWITTER_USERNAME	= ''
TWITTER_PASSWORD	= ''

DATETIME_FORMAT 	= '%a %b %d %H:%M:%S +0000 %Y'
TIMEDELTA			= -7

LOG_DIR				= "log"
SINCE_ID_FILENAME	= LOG_DIR + "/since_id.log"

def getLastID():
	if( os.path.isfile(SINCE_ID_FILENAME) ):		
		f = open(SINCE_ID_FILENAME, 'r')
		last_id = f.read()
		f.close()
		return last_id
	else:
		return 0

def writeLastID(since_id):
	f = open(SINCE_ID_FILENAME, 'w')
	f.write(since_id)
	f.close()

def writeStatuses(statues):
	for status in reversed(statues):
		created_at = datetime.datetime.strptime(status.created_at, DATETIME_FORMAT ) + datetime.timedelta(hours=TIMEDELTA)
		created_date = created_at.date()
		log_file = LOG_DIR + '/' + str(created_date) + '.log'
		f = codecs.open(log_file, 'a', 'utf-8')
		output_text = status.text + ' ' + created_at.strftime("%H:%M:%S") + '\n'
		print output_text
		f.write(output_text)
		f.close()

def main():
	# create working directory
	if( not os.path.isdir(LOG_DIR) ):
		os.mkdir(LOG_DIR)
	
	# create twitter api client
	twitter_api = twitter.Api(username=TWITTER_USERNAME, password=TWITTER_PASSWORD)
	
	since_id = getLastID()
	since_id = 0 # for debug
	statuses = twitter_api.GetUserTimeline('drikin', since_id=since_id)
	if( statuses ):
		writeStatuses(statuses)
		writeLastID(str(statuses[0].id))

if __name__ == '__main__':
	main()

