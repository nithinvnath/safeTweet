#! /usr/bin/python

#code to read the classes only from an arfffile and compare it with the label file
import tweepy
import cPickle as pickle

frawtweets = open('../Dataset/Raw-Tweets/raw-tweets11.dat','r')
flabelled = open("../Dataset/test11_labeled.arff",'r')
factuallabel = open("../Dataset/Raw-Tweets/label11.txt",'r')
correct=0
incorrect=0
count=1
while(count<12):
	flabelled.readline()
	count=count+1
	
statuses = pickle.load(frawtweets)
while statuses is not None:
	for tweet in statuses:
		actuallabel = factuallabel.readline().strip()
		if actuallabel=="Ignore":
			continue
		x=flabelled.readline()
		classifiedlabel = x.rsplit(",",1)[1].strip()
		if classifiedlabel != actuallabel:
			print "Classified as: ",classifiedlabel, "| Actual class: ", actuallabel
		if classifiedlabel == actuallabel:
			correct = correct + 1
		else:
			incorrect = incorrect + 1
			print incorrect,") ",x.rsplit(",",1)[1].strip()," -->",tweet.user.name+": "+tweet.text+"\n"
	try:
		statuses = pickle.load(frawtweets)
	except EOFError:
		break
print "Incorrect = ", incorrect,"\nCorrect =",correct