import sys
import json
import re

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

def print_frequency(tweet_file):
	tweets = load_tweets(tweet_file)
	parsed = parse_tweets(tweets)
	terms = {}
	for words in parsed:
		for w in words:
			terms[w] = terms[w]+1 if w in terms.keys() else 1

	freq_all = sum([v for (k,v) in terms.items()])
	freqs = map(lambda (k,v): { k: float(v)/freq_all }, terms.items())

	for d in freqs:
		print "%s %s" % (d.items()[0])

def main():
    tweet_file = open(sys.argv[1])

    print_frequency(tweet_file)

    tweet_file.close()

if __name__ == '__main__':
    main()