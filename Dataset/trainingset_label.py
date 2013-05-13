#! /usr/bin/python

""" Reads tweets from a file and removes the stopwords
Assumes the tweets are of the form <username>: <tweet>"""

import tweepy
import cPickle as pickle

import unicodedata
import sys

import re
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer



wnl = WordNetLemmatizer()
#---------------------------------------------------------------------#
#Function that takes as input a line and removes stopwords from it
def removeStopwords (line):
	words = re.findall(r'\w+', line,flags = re.UNICODE | re.LOCALE) 
	important_words = []
	for word in words:
		if word not in stopwords.words('english'):
			word = wnl.lemmatize(word)
			important_words.append(word)
	return important_words

def stemming(line):
	stemmer = PorterStemmer()
	line_array = line.split(" ")
	for word in line_array:
		replace_word = stemmer.stem(word)
		#print replace_word	
		line = line.replace(word,replace_word)
	return line

def removePunctuation(text):
    return re.sub(ur"\p{P}+", "", text)


def hasUrl (tweet):
	#u=re.compile('http\:\/\/t\.co\/[a-zA-Z0-9]+')
	#return u.findall(line)
	if tweet.entities['urls'] == []:
		return 0
	else:
		return 1


def hasUsernames(tweet):
	#u=re.compile('\@[a-zA-Z0-9\_]+')
	#return u.findall(line)
	if tweet.entities['user_mentions'] == []:
		return 0
	else:
		return 1
def verifiedUser(user):
	if user.verified is True:
		return 1
	else:
		return 0

def emphExist(line):
	presence = 0
	emp_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
	words = line.split()
	for word in words:
		if emp_regexp.match(word) is not None:
			if wordnet.synsets(word):
				continue
			else:
				presence = presence +1
	return presence


def emphReplace(line):
	words = re.findall(r'\w+', line,flags = re.UNICODE | re.LOCALE) 
	for word in words:
		new_word=emphReplaceWord(word)
		line=line.replace(word,new_word)
	return line


def emphReplaceWord(word):
	emp_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
	if wordnet.synsets(word):
		return word
	matched = emp_regexp.match(word)
	if matched is None:
		return word
	word = matched.group(1)+matched.group(2)+matched.group(3)
	return emphReplaceWord(word)



def isRetweet(tweet):
	# p = re.compile('([A-Za-z\ ]+\:)(\\t)(.*)')
	# m = p.match(tweet)
	# t = m.group(3)
	# if (t[0]=='R' and t[1]=='T' and t[2]==' '):
	# 	return 1
	# else:
	# 	return 0
	if hasattr(tweet,'retweeted_status'):
		return 1
	else:
		return 0

def hasProfanity(words):
	count = 0
	f = open('../Corpus/profanity-stemmed.txt','r')
	lis = []
	for badword in f:
		lis.append(badword.strip())
	for badword in lis:
		if badword in words:
			count = count + 1
	return count

def hasExplicit(words):
	count = 0
	f = open('../Corpus/explicit-stemmed.txt','r')
	lis = []
	for badword in f:
		lis.append(badword.strip())
	for badword in lis:
		if badword in words:
			count = count + 1
	return count

def hasHateSpeech(words):
	count = 0
	f = open('../Corpus/hate-speech-stemmed.txt','r')
	lis = []
	for badword in f:
		lis.append(badword.strip())
	for badword in lis:
		if badword in words:
			count = count + 1
	return count

def hasPhoto(tweet):
	try:
		tweet.entities['media']
		return 1
	except:
		return 0

def hasBadWord(words):
	count = 0
	f = open('../Corpus/bad-words-stemmed.txt','r')
	lis = []
	for badword in f:
		lis.append(badword.strip())
	for badword in lis:
		if badword in words:
			count = count + 1
	return count

def retweetCount(tweet):
	return tweet.retweet_count

frawtweets = open('./Raw-Tweets/raw-tweets23.dat','r')
foutput = open('../Weka/trainingset.arff','w')
flabel = open('./Raw-Tweets/label23.txt','r')

if foutput.tell()==0:
	foutput.write("@RELATION safe-tweets\n\n")
	# foutput.write("@ATTRIBUTE hasUrl \t NUMERIC \n")
	foutput.write("@ATTRIBUTE verifiedUser \t NUMERIC \n")
	# foutput.write("@ATTRIBUTE Mentions \t NUMERIC \n")
	# foutput.write("@ATTRIBUTE Emphasis \t NUMERIC \n")
	# foutput.write("@ATTRIBUTE Retweet \t NUMERIC \n")
	foutput.write("@ATTRIBUTE Profanity \t NUMERIC \n")
	foutput.write("@ATTRIBUTE Explicit \t NUMERIC \n")
	foutput.write("@ATTRIBUTE HateSpeech \t NUMERIC \n")
	foutput.write("@ATTRIBUTE hasPhoto \t NUMERIC \n")
	foutput.write("@ATTRIBUTE RetweetCount \t NUMERIC \n")
	foutput.write("@ATTRIBUTE class \t{Safe, Unsafe}\n\n")
	foutput.write("@DATA\n\n")

print("Safe or Unsafe or Ignore (S/U/Ignore)?")
statuses = pickle.load(frawtweets)
count = 0
while statuses is not None:
	for tweet in statuses:
		s = flabel.readline()
		isSafe=s.strip()
		if isSafe=="Ignore":
			count = count + 1
			print "Ignored"
			continue
		#isSafe="?"		#uncomment this line to create a file to label
		tweet_text=removePunctuation(tweet.text.lower())
		tweet_text=tweet_text+" "+tweet.user.name.lower()
		tweet_text=stemming(tweet_text)
		#tweet_vector = str(hasUrl(tweet)) + "," 
		tweet_vector=str(verifiedUser(tweet.user)) #+"," +str(hasUsernames(tweet))
		#tweet_text = removePunctuation(tweet.text.lower())
		#tweet_vector = tweet_vector +","+ str(emphExist(tweet_text)) + "," +str(isRetweet(tweet))
		tweet_words = removeStopwords(tweet_text)
		tweet_vector = tweet_vector + ","+ str(hasProfanity(tweet_words))+ ","+ str(hasExplicit(tweet_words))+ ","+ str(hasHateSpeech(tweet_words))
		tweet_vector = tweet_vector +","+str(hasPhoto(tweet))+","+str(retweetCount(tweet))
		tweet_vector = tweet_vector + "," +isSafe+ "\n"
		#print count, tweet.text, " "+tweet_vector+"\n"+tweet_vector
		foutput.write(tweet_vector.encode("UTF-8"))
		count = count + 1
	try:
		statuses = pickle.load(frawtweets)
	except EOFError:
		print count, "Finished"
		break
foutput.close()
frawtweets.close()
flabel.close()
