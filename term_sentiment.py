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
    tweets = jsonTweets(tweet_file)
    words = getTextFromTweets(tweets)
    noScoreWords = {}
    for phrase in words:
	p,n = (0,0)
	zeroScore=[]
	for w in phrase:
	    score = getScoreFromDict(scores,w)
	    if score < 0: n = n + 1
	    elif score > 0: p = p + 1
	    else: zeroScore.append(w)
	if n is not 0:
	    ratio = float(p)/n
	else:
	    ratio = p
	for term in zeroScore:
	    if term in noScoreWords.keys():
		noScoreWords[term] = noScoreWords[term] + ratio
	    else:
		noScoreWords[term] = ratio	
    for k,v in noScoreWords.items():
	print "%s %s" % (k, v)



if __name__ == '__main__':
    main()
