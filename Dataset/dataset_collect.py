#! /usr/bin/python

#Collect 20 tweets each from each user.
#Takes as input a text file containing usernames.
#Needs a twitter application and twitter login

import tweepy
from webbrowser import open as webopen
import pickle	#for writing and reading objects directly to files

#Consumer token and secret are specific to the application
#Can  be found in dev.twitter.com/apps
consumer_token = "pDeVZbNzK6HXocUuhwLqBg"
consumer_secret = "Itj45FWSmMr0VmrNPJuO2KIaIt3hzayY2ywVteh2M"
auth = tweepy.OAuthHandler(consumer_token,consumer_secret)
auth_url = auth.get_authorization_url(signin_with_twitter=True)
#the following access token is specific to a user
#used to avoid the OAuth handshake everytime the prgram runs
access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)
print "Authenticated"
fusersfile = open('./User-lists/user-list.txt','r')		#User names list
fuserdetail = open('./User-lists/user-details.txt','a')	#details of user are stored in case we need it later
pickle.HIGHEST_PROTOCOL
frawtweets = open('./Raw-Tweets/raw-tweets.dat','a')		#the tweepy tweet object is directly saved into this file
count = 1
for user_name in fusersfile:
	try:
		user=api.get_user(user_name)
		pickle.dump(user,fuserdetail)
		status_list=api.user_timeline(user_name)
		pickle.dump(status_list,frawtweets)
		print str(count) + ". " + user_name
		count = count+1
	except tweepy.error.TweepError,e:
		print user_name + e.reason 
fusersfile.close()
frawtweets.close()
fuserdetail.close()
