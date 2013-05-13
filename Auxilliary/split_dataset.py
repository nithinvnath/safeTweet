#! /usr/bin/python

import tweepy
import cPickle as pickle

#splits a single raw tweet file to multiple files
#to help in dividing the labelling work to different people

frawtweets=open('../Dataset/Raw-Tweets/raw-tweets.dat','r')
fsplit1=open('../Dataset/Raw-Tweets/raw-tweets1.dat','a')
fsplit2=open('../Dataset/Raw-Tweets/raw-tweets2.dat','a')
fsplit3=open('../Dataset/Raw-Tweets/raw-tweets3.dat','a')
fsplit4=open('../Dataset/Raw-Tweets/raw-tweets4.dat','a')
fsplit5=open('../Dataset/Raw-Tweets/raw-tweets5.dat','a')

count = 1

statuses = pickle.load(frawtweets)
while statuses is not None:
	print count
	if count<=15:
		pickle.dump(statuses,fsplit1)
	else:
		if count<=30:
			pickle.dump(statuses,fsplit2)
		else:
			if count<=45:
				pickle.dump(statuses,fsplit3)
			else:
				if count<=60:
					pickle.dump(statuses,fsplit4)
				else:
					pickle.dump(statuses,fsplit5)
	statuses=pickle.load(frawtweets)
	count = count+1;

frawtweets.close()
fsplit1.close()
fsplit2.close()
fsplit3.close()
fsplit4.close()
fsplit5.close()
