#! /usr/bin/python

#Stems the corpus.
#otherwise we have to stem each word after reading it from file

from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

wnl = WordNetLemmatizer()

def stemming(word):
	stemmer = PorterStemmer()
	replace_word = stemmer.stem(word)
	print word,"-->", replace_word
	return replace_word

fcorpus = open('../Corpus/hate-speech.txt','r')
foutput = open('../Corpus/hate-speech-stemmed.txt','w')

word = fcorpus.readline()
count =0
while count < 400:
	replace_word = stemming(word.strip())
	foutput.write(replace_word+"\n")
	word=fcorpus.readline()
	count = count+1
	if word=="\n":
		break
fcorpus.close()
foutput.close()
