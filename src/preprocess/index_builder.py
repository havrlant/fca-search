from collections import Counter
from common.funcfun import lmap
from functools import reduce
from operator import add
from preprocess.words import get_words
from preprocess.html_remover import HTMLRemover
from common.string import normalize_text
from html.parser import HTMLParseError

def getinfo(documents):
	counters = list(enumerate(map(lambda x: Counter(x), documents)))
	allwords = reduce(add, documents)
	allwords_counter = Counter(allwords)
	words = sorted(set(allwords))
	occurencesIndex = lmap(lambda x: ((x, allwords_counter[x]), occurences(counters, x)), words)
	wordscount = lmap(len, documents)
	return {'allwords' : allwords_counter, 'occurences' : occurencesIndex, 'wordscount' : wordscount}

def occurences(counters, word):
	return lmap(lambda x: (x[0], x[1][word]), filter(lambda x: word in x[1], counters))

def group(database, keylen):
	dic = {}
	for record in database:
		key = record[0][0][:keylen]
		if key in dic:
			dic[key].append(record)
		else:
			dic[key] = [record]
	return dic

def toindex(sites, urls, stopwords, keylen):
	htmlrem = HTMLRemover()
	parsedSites = []
	correctUrl = []
	
	for site, url in zip(sites, urls):
		try:
			parsedSites.append(get_words(normalize_text(htmlrem.compile(site)), stopwords))
			correctUrl.append(url)
		except HTMLParseError:
			print('Cannot parse ' + str(url))
	
	sitesInfo = getinfo(parsedSites)
	index = group(sitesInfo['occurences'], keylen)
	
	return {'index': index, 'allwords':sitesInfo['allwords'], 'urls': correctUrl, 'wordscount':sitesInfo['wordscount']}