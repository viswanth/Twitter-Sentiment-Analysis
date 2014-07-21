import sys
import json
import re

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def getDict(fp):
    afinnfile = open(sys.argv[1])
    scores = {}
    for line in afinnfile:
	term, score = line.split("\t")
	scores[term] = int(score)
    return scores

def getScoreFromDict(d, word):
    return d.get(word,0)

def jsonTweets(fp):
    alltweets = []
    for line in fp:
	if len(line) is not 0:
	    line = line.strip()
	    alltweets.append(json.loads(line))
	else:
	    continue
    return alltweets

def getTextFromTweets(tweets):
    regExp = re.compile(r'\w+')
    words = []
    for tweet in tweets:
	if 'text' in tweet.keys():
	    textWords = regExp.findall(tweet['text'])
	    words.append(textWords)
        else:
	    continue
    return words

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
    scores = getDict(sent_file)
    #print len(scores)
    tweets = jsonTweets(tweet_file)
    words = getTextFromTweets(tweets)
    for phrase in words:
	tweetScore = 0
	for w in phrase:
	    tweetScore = tweetScore + getScoreFromDict(scores,w)
	print tweetScore

if __name__ == '__main__':
    main()
