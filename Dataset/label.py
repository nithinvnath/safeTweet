#! /usr/bin/python

import tweepy
import cPickle as pickle

frawtweets = open('./Raw-Tweets/raw-tweets.dat','r')
flabel=open('../Raw-Tweets/label.txt','a')
fcount = open('count.txt','r')		#must be present before starting the script
print("Safe or Unsafe or Ignore (S/U/I) (Enter Q at anytime to quit)?")
#quitting saves the labelling done so far. can continue any time later
fcount.seek(0,2)
if fcount.tell()==0:
	seekpos=0
	seekcount=0
else:
	fcount.seek(0)
	seekpos=fcount.readline()
	seekpos=seekpos.strip()
	seekpos=int(seekpos)
	print seekpos
	seekcount=fcount.readline()
	seekcount=seekcount.strip()
	seekcount=int(seekcount)
	print seekcount

fcount.close()
fcount = open('count.txt','w')

statuses = pickle.load(frawtweets)
flag=1
count=0
pos=0
while ((statuses is not None) and (flag == 1)):
	if(pos<seekpos):
		pos=pos+1
		statuses = pickle.load(frawtweets)
		continue
	for tweet in statuses:
		if(count<seekcount):
			count=count+1
			continue
		else:
			seekcount=0
		tweet_text = str(pos)+"-"+str(count)+"=> "+tweet.user.name+": "+tweet.text+" (S/U/I/Q)?"
		s = raw_input(tweet_text.encode("UTF-8"))
		if(s=='Q' or s=='q'):
			flag=0
			fcount.write(str(pos)+"\n"+str(count))
			fcount.close()
			break
		if(s=='S' or s=='s'):
			label="Safe\n"
		else:
			if(s=='U' or s=='u'):
				label = "Unsafe\n"
			else:
				label="Ignore\n"
		flabel.write(label)
		count = count+1
	try:
		statuses = pickle.load(frawtweets)
	except EOFError:
		print "\n********Completed********"
		break
	count=0
	pos=pos+1

frawtweets.close()
flabel.close()


	
