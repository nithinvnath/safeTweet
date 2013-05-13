#! /usr/bin/python

""" Reads tweets from a file and removes the stopwords
Assumes the tweets are of the form <username>: <tweet>"""

import tweepy
from webbrowser import open as webopen

import re
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

#---------------------------------------------------------------------#
#							TWITTER API								  #
#---------------------------------------------------------------------#

# #Consumer token and secret are specific to the application
# #Can  be found in dev.twitter.com/apps
# consumer_token = "pDeVZbNzK6HXocUuhwLqBg"
# consumer_secret = "Itj45FWSmMr0VmrNPJuO2KIaIt3hzayY2ywVteh2M"

# #To get authorization from user using OAuth
# auth = tweepy.OAuthHandler(consumer_token,consumer_secret)
# auth_url = auth.get_authorization_url(signin_with_twitter=True)

# # print "Authorize: " + auth_url
# webopen(auth_url)
# verifier = raw_input('PIN: ').strip()
# auth.get_access_token(verifier)

# access_token = auth.access_token.key
# access_secret = auth.access_token.secret
# # access_token = "45142783-KrrjDjWf0M3OKuq1Ckb9Bi6WpNX9ZQnhurPM1wxDA"
# # access_secret = "b6a6OHD39u1GNJMfkTp5LGRWCk7WWgTZgPkE6sgp8wo"

# #Access the user's account using the OAuth credentials
# auth.set_access_token(access_token,access_secret)

# api = tweepy.API(auth)	#authenticated api module

# if api.me().name is not None:
# 	print "Successfully authenticated"
# else:
# 	print "Authentication failed!"

# pub = api.home_timeline()

#--------------------------------------

consumer_token = "pDeVZbNzK6HXocUuhwLqBg"
consumer_secret = "Itj45FWSmMr0VmrNPJuO2KIaIt3hzayY2ywVteh2M"
auth = tweepy.OAuthHandler(consumer_token,consumer_secret)
auth_url = auth.get_authorization_url(signin_with_twitter=True)
access_token = "45142783-KrrjDjWf0M3OKuq1Ckb9Bi6WpNX9ZQnhurPM1wxDA"
access_secret = "b6a6OHD39u1GNJMfkTp5LGRWCk7WWgTZgPkE6sgp8wo"
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)
pub = api.home_timeline()

#---------------------------------------------------------------------#
#							PREPROCESSING							  #
#---------------------------------------------------------------------#


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

#---------------------------------------------------------------------#
#							INDEXING								  #
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
#Twitter converts all urls to http://t.co/<something>
#Checks for presence of URL using API. Takes as input a tweet object


def hasUrl (tweet):
	#u=re.compile('http\:\/\/t\.co\/[a-zA-Z0-9]+')
	#return u.findall(line)
	if tweet.entities['urls'] == []:
		return 0
	else:
		return 1


#---------------------------------------------------------------------#
#function to check the presence of a username in the 
#tweet


def hasUsernames(tweet):
	#u=re.compile('\@[a-zA-Z0-9\_]+')
	#return u.findall(line)
	if tweet.entities['user_mentions'] == []:
		return 0
	else:
		return 1

#---------------------------------------------------------------------#
#Function to check if the author of tweet is verified user or not

def verifiedUser(user):
	if user.verified is True:
		return 1
	else:
		return 0


#---------------------------------------------------------------------#
#function to find emphasis on words by repetition of
#letters

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



#replaces the word after removing repeated letters
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

#---------------------------------------------------------------------#
#checks if the tweet is a retweet
#takes as input tweet object
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


#---------------------------------------------------------------------#
#checks for presence of profanity. Compares each word from file 'bad-words.txt'
#expects a list of words
def hasProfanity(words):
	count = 0
	f = open('./Corpus/profanity.txt','r')
	lis = []
	for badword in f:
		lis.append(badword.strip())
	for badword in lis:
		if badword in words:
			count = count + 1
	return count

def hasExplicit(words):
	count = 0
	f = open('./Corpus/explicit.txt','r')
	lis = []
	for badword in f:
		lis.append(badword.strip())
	for badword in lis:
		if badword in words:
			count = count + 1
	return count

def hasHateSpeech(words):
	count = 0
	f = open('./Corpus/hate-speech.txt','r')
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

def retweetCount(tweet):
	return tweet.retweet_count
#---------------------------------------------------------------------#
#The following regular expression checks for three groups
#name followed by a colon, a tab and finally the tweet
# p = re.compile('([a-z\ ]+\:)(\\t)(.*)',re.IGNORECASE)
# f = open('test','rb')
# for tweet in f:
# 	m = p.match(tweet)
# 	if m is not None:		#the file may contain invalid contents
# 		print tweet
# 		print hasUsernames(tweet)
# 		#print removeStopwords(m.group(3))
# f.close()

#Feature Vector: [hasUrl, verifiedUser, hasUsername,emphExist,isRetweet,Profanity,Explicit,HateSpeech]

i=0

#for tweet in pub:
	# fvector[i][0] = hasUrl(tweet)
	# fvector[i][1] = verifiedUser(tweet)
	# fvector[i][2] = hasUsernames(tweet)
	# tweet_text = tweet.text
	# fvector[i][3] = emphExist(tweet_text)
	# fvector[i][4] = isRetweet(tweet_text)
	# tweet_words = removeStopwords(tweet_text)
	# fvector[i][5] = hasProfanity(tweet_words)
	# fvector[i][6] = hasExplicit(tweet_words)
	# fvector[i][7] = hasHateSpeech(tweet_words)
	# print fvector[i]
tweet = pub[1]
print tweet.text
print "URL: ", hasUrl(tweet)
print "User: ", verifiedUser(tweet.user)
print "Mentions: ", hasUsernames(tweet)
tweet_text = removePunctuation(tweet.text.lower())
print "Emphasis: ", emphExist(tweet_text)
print "Retweet: ", isRetweet(tweet)
tweet_text = emphReplace(tweet_text)
tweet_words = removeStopwords(tweet_text)
print "Profanity: ", hasProfanity(tweet_words)
print "Explicit: ", hasExplicit(tweet_words)
print "HateSpeech: ", hasHateSpeech(tweet_words)
#print fvector[i]
print "******************************************"