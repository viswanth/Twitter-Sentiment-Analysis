import time
import sys
import json
import re

state_mapping = { 
	"alabama": "al",
	"alaska": "ak",
	"arizona": "az",
	"arkansas": "ar",
	"california": "ca",
	"colorado": "co",
	"connecticut": "ct",
	"delaware": "de",
	"florida": "fl",
	"georgia": "ga",
	"hawaii": "hi",
	"idaho": "id",
	"illinois": "il",
	"indiana": "in",
	"iowa": "ia",
	"kansas": "ks",
	"kentucky": "ky",
	"louisiana": "la",
	"maine": "me",
	"maryland": "md",
	"massachusetts": "ma",
	"michigan": "mi",
	"minnesota": "mn",
	"mississippi": "ms",
	"missouri": "mo",
	"montana": "mt",
	"nebraska": "ne",
	"nevada": "nv",
	"new hampshire": "nh",
	"new jersey": "nj",
	"new mexico": "nm",
	"new york": "ny",
	"north carolina": "nc",
	"north dakota": "nd",
	"ohio": "oh",
	"oklahoma": "ok",
	"oregon": "or",
	"pennsylvania": "pa",
	"rhode island": "ri",
	"south carolina": "sc",
	"south dakota": "sd",
	"tennessee": "tn",
	"texas": "tx",
	"utah": "ut",
	"vermont": "vt",
	"virginia": "va",
	"washington": "wa",
	"west virginia": "wv",
	"wisconsin": "wi",
	"wyoming": "wy" }

token_regex = re.compile(r'\w+')
abbr_state_regex = re.compile(r'\w{2}')

class SentimentScore(object):
	_lookup = None

	def __init__(self, sent_file):
		if SentimentScore._lookup is None:
			SentimentScore._lookup = self._build_lookup(sent_file)

	def _build_lookup(self, sent_file):
		scores = {} # initialize an empty dictionary
		for line in sent_file:
		  term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
		  scores[term] = int(score)  # Convert the score to an integer.

		return scores

	def get_score(self, word):
		return self._lookup.get(word, 0)

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
	"""
	Parses a list of tweets, splitting the ``text`` of the tweet into tokens 
	based on a regular expression.  If there is no ``text`` property then
	an empty list is returned.
	"""

	if 'text' not in tweet.keys():
		return []

	# Obtain a list of words
	return token_regex.findall(tweet['text'])

def parse_user_loc(tweet, abbr_states):
	"""
	Checks for both state abbreviations (from set ``abbr_states``) and full
	names of states in the User ``location`` property.  

	Returns empty list if no full state name or abbreviation is found.
	"""
	tokens = token_regex.findall(tweet['user']['location'])
	abbr_state = filter(lambda t: t in abbr_states, tokens)

	if not len(abbr_state) is 0:
		# Found a state abbreviation, return it.
		return abbr_state[0]

	# Check for full state names
	states = filter(lambda t: t in state_mapping.keys(), tokens)

	if not len(states) is 0:
		# Found a full state, return the abbreviation
		state = states[0]
		return state_mapping[state]

	return None

def print_happy_state(sent_file, tweet_file):
	scores = SentimentScore(sent_file)
	tweets = filter(lambda t: 'delete' not in t.keys(), jsonTweets(tweet_file))
	abbr_states = set(map(lambda (k,v): v, state_mapping.items()))
	state_scores = dict.fromkeys(abbr_states, 0)
	state_tweets = filter(
		lambda t: 'place' in t.keys() \
			and t['place'] is not None \
			and t['place']['name'].lower() in state_mapping.keys(), tweets)
	state_tweet_ids = set(map(lambda t: t['id'], state_tweets))
	rest_tweets = filter(lambda t: t['id'] not in state_tweet_ids, tweets)

	if len(state_tweets) > 0:
		rest_tweets.extend(state_tweets)

	for t in rest_tweets:
		text =  parse_tweet(t)
		if len(text) is 0:
			continue

		score = sum([scores.get_score(w) for w in text])

		if t['id'] in state_tweet_ids:
			state = t['place']['name'].lower()
			key = state_mapping[state]
		else:
			key = parse_user_loc(t, abbr_states)
			if key is None: 
				continue
		state_scores[key] = state_scores[key] + score

	sent_max = 0
	happy_state = ""
	for (k,v) in state_scores.items():
		if v > sent_max:
			sent_max = v
			happy_state = k

	print happy_state.upper()

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    print_happy_state(sent_file, tweet_file)

    sent_file.close()
    tweet_file.close()

if __name__ == '__main__':
    main()