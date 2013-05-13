#! /usr/bin/python

import tweepy
import cPickle as pickle

frawtweets2=open('../Dataset/Raw-Tweets/raw-tweets2.dat','r')
frawtweets3=open('../Dataset/Raw-Tweets/raw-tweets3.dat','r')

foutput = open('../Dataset/Raw-Tweets/raw-tweets23.dat','w')

statuses = pickle.load(frawtweets2)
count = 0
while statuses is not None:
	pickle.dump(statuses,foutput)
	try:
		statuses = pickle.load(frawtweets2)
	except EOFError:
		print count, "Finished 2"
		break

statuses = pickle.load(frawtweets3)
count = 0
while statuses is not None:
	pickle.dump(statuses,foutput)
	try:
		statuses = pickle.load(frawtweets3)
	except EOFError:
		print count, "Finished 2"
		break

foutput.close()
frawtweets3.close()
frawtweets2.close()