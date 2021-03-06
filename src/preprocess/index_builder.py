from collections import Counter
from common.string import strip_html
from common.string import unescapeHTMLEntities
from common.funcfun import lmap, nothing
from functools import reduce
from operator import add
from preprocess.words import getstem, getWordsWithoutStopWords, stemAndRemoveAccents, stripAccents
from preprocess.html_remover import HTMLRemover
from common.string import normalize_text
from retrieval.ranking import document_score
import os

def getDocsStats(documents):
	counters = list(enumerate(map(lambda x: Counter(x), documents)))
	allwords = reduce(add, documents, [])
	allwords_counter = Counter(allwords)
	words = sorted(set(allwords))
	occurencesIndex = lmap(lambda x: ((x, allwords_counter[x]), occurences(counters, x)), words)
	wordscount = lmap(len, documents)
	return {'allwords' : allwords_counter, 'occurences' : occurencesIndex, 'wordscount' : wordscount}

def occurences(counters, word):
	return lmap(lambda x: (x[0], x[1][word]), filter(lambda x: word in x[1], counters))

def groupByKeylen(database, keylen):
	dic = {}
	for record in database:
		key = record[0][0][:keylen]
		if key in dic:
			dic[key].append(record)
		else:
			dic[key] = [record]
	return dic

def getKeywords(documents, index, elapsed, lang):
	keywords = []
	for doc in documents:
		elapsed('getting keywords from ' + doc['url'])
		distContent = set(doc['content']) #{getstem(x, lang) for x in set(doc['content'])}
		keyValues = {}
		for stem in distContent:
			keyValues[stem] = round(document_score([stem], doc['id'], index, doc['words']), 8)
			
		foo = sorted(keyValues.items(), key=lambda x: x[1], reverse = True)
		keywords.append(foo)
	return keywords

def toIndex(documents, stopwords, keylen, lang, elapsed = nothing):
	htmlrem = HTMLRemover()	
	compiledDocuments = []
	docID = 0
	allRealWords = set()
	
	for doc in documents:
		try:
			elapsed('parsing: ' + doc['url'])

			if doc['type'] in ['html', 'txt']:
				if doc['type'] == 'html':
					content = unescapeHTMLEntities(doc['content'])

					try:
						content = htmlrem.getText(content)
					except Exception:
						content = strip_html(content)
					
					title = htmlrem.title
					description = htmlrem.description

					if not title:
						title = os.path.basename(doc['url'])

				if doc['type'] == 'txt':
					content = doc['content']
					title = doc.get('title', os.path.basename(doc['url']))
					description = doc.get('description', '')

				words = getWordsWithoutStopWords(normalize_text(content), stopwords)
				allRealWords |= stripAccents(words)

				if words:
					compiledDocuments.append({
							'pureContent':words,
							'content':stemAndRemoveAccents(words, lang), 
							'title':title,
							'url':doc['url'], 
							'id':docID, 
							'description':description,
							})

					docID += 1
		except Exception as err:
			print('Cannot parse ' + str(doc['url']))
			print(str(err))

	if not compiledDocuments:
		raise Exception('No document parsed')
	
	elapsed('Collecting documents...')
	sitesStats = getDocsStats([x['content'] for x in compiledDocuments])
	
	for doc, wordscount in zip(compiledDocuments, sitesStats['wordscount']):
		doc['words'] = wordscount
	
	index = groupByKeylen(sitesStats['occurences'], keylen)
	
	return {'index': index, 'allwords':sitesStats['allwords'], 
			'documents':compiledDocuments, 'allRealWords':allRealWords}