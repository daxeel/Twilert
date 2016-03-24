#! /usr/bin/env python
#
# SCRIPT NAME  : Twilert
# DESCRIPTION  : Simple python script for real time desktop twitter hashtag tweet alert notification.
# AUTHOR       : Daxeel Soni
# AUTHOR EMAIL : sayhi@daxeelsoni.in
# AUTHOR WEB   : www.daxeelsoni.in
#
# Copyright (c) 2016, Daxeel Soni
# All rights reserved.

# Import modules
import urllib2
from bs4 import BeautifulSoup
import pickledb
from pync import Notifier
import sys

def get_tweet(hashtag):

	url = "https://twitter.com/hashtag/" + hashtag + "?f=tweets&vertical=default"  # Build twitter hashtag url
	req = urllib2.urlopen(url) # URL request
	soup = BeautifulSoup(req, "html.parser") # Make beautiful soup

	recent_tweet = str(soup.find_all('p', {'class': 'TweetTextSize  js-tweet-text tweet-text'})) # Get recent tweet

	# Check for new tweet 
	if db.get('latest_tweet') != len(recent_tweet):
		db.set('latest_tweet', len(recent_tweet)) 
		recent_username = soup.find_all('span', {'class': 'username js-action-profile-name'})[0].b.string
		
		print recent_username # Print username

		tweet_id = soup.find_all('div', {'class': 'stream'})[0].ol.li['data-item-id'] # Get id of recent tweet
		tweet_url = "https://twitter.com/" + recent_username + "/status/" + tweet_id # Build url for recent tweet

		Notifier.notify('New tweet by '+recent_username, title='Twilert', open=tweet_url) # Push desktop notification for new tweet

args = sys.argv
if len(args) == 3:
	if args[1] == "--hashtag":
		# Create db
		db = pickledb.load('track_tweet.db', True) 
		# Continous loop for checking new tweet
		while True:
			print "checking..."
			get_tweet(args[2]) # Specify hashtag for which you want to get tweets in get_tweet function
	else:
		print "Invalid syntax. Please read the docs at https://github.com/daxeel/Twilert"
else:
	print "Invalid arguments passed. Please read the docs at https://github.com/daxeel/Twilert"
