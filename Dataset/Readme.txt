Raw-Tweets/ -> contains the tweets (saved as Tweepy objects)
User-lists/ -> list of users from whom the dataset is to be collected

datset_collect.py -> collects datset from twitter
label.py -> to manually label the collected dataset
trainingset_label.py -> uses the labelling from label.py to create an ARFF file that can be used by WEKA
---
findtweetcount.py -> to count the number of tweets in a .dat file
