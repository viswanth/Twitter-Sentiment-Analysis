import sys
import json

def jsonTweets(fp):
    alltweets = []
    for line in fp:
	if len(line) is not 0:
	    line = line.strip()
	    alltweets.append(json.loads(line))
	else:
	    continue
    return alltweets

def parse_tweet(tweet):
	if 'text' not in tweet.keys():
		return []
	return token_regex.findall(tweet['text'])

def print_top_ten(tweet_file):
	tweets = filter(lambda t: 
		'delete' not in t.keys() and \
		not len(t['entities']['hashtags']) is 0, jsonTweets(tweet_file))
	hash_scores = {}

	for tweet in tweets:
		for h in tweet['entities']['hashtags']:
			key = h['text']
			hash_scores[key] = hash_scores[key] + 1.0 if key in hash_scores.keys() else 1.0

	sorted_scores = sorted(hash_scores.items(), key=lambda x: x[1])[0:10]

	for k, v in sorted_scores:
		print "%s %s" % (k, v)

def main():
    tweet_file = open(sys.argv[1])

    print_top_ten(tweet_file)

    tweet_file.close()

if __name__ == '__main__':
    main()