from collections import Counter
from common.funcfun import lmap
from functools import reduce
from operator import add


class Database:
	def getinfo(self, documents):
		counters = list(enumerate(map(lambda x: Counter(x), documents)))
		allwords = reduce(add, documents)
		allwords_counter = Counter(allwords)
		words = sorted(set(allwords))
		occ = lmap(lambda x: ((x, allwords_counter[x]), self.occurences(counters, x)), words)
		return occ
	
	def occurences(self, counters, word):
		return lmap(lambda x: (x[0], x[1][word]), filter(lambda x: word in x[1], counters))