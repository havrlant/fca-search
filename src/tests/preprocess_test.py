import unittest
from preprocess.words import towords, remstopwords
from common.io import readfiles, readfile
from common.funcfun import lmap
from preprocess.index_builder import toindex

class TestWords(unittest.TestCase):
	testFolder = '../../files/tests/'
	
	def test_towords(self):
		self.assertEquals(['Každému', 'svítání', 'předchází', 'hluboká', 'tma...'], towords('Každému svítání předchází hluboká tma...'))
		self.assertEquals([''], towords(''))
		
	def test_remstopwords(self):
		words = 'Van Rossum was born and grew up in the Netherlands, where he received a masters degree in mathematics and computer science'.split()
		self.assertEquals(['Rossum', 'born', 'grew', 'the', 'Netherlands,', 'where', 'received', 'masters', 'degree', 'mathematics', 'computer', 'science'], list(remstopwords(words, ['Van', 'was', 'up', 'in', 'and', 'he', 'a'])))
		self.assertEquals(['Van', 'Rossum', 'was', 'born', 'and', 'grew', 'up', 'in', 'the', 'Netherlands,', 'where', 'he', 'received', 'a', 'masters', 'degree', 'in', 'mathematics', 'and', 'computer', 'science'], list(remstopwords(words, [])))
		self.assertEquals(['a', 'b'], list(remstopwords(['a', 'b'], ['c'])))
		
	def test_toindex(self):
		urls = ['binomicka-veta.html', 'prirozena-cisla.html', 'pythagorova-veta.html', 'rovnice.html', 'zaklady-statistiky.html']
		sites = readfiles(lmap(lambda x: self.testFolder + 'sites/' + x, urls))
		result = toindex(sites, urls, [], 1)
		desired = readfile(self.testFolder + '/results/index1.txt')
		self.assertEquals(repr(result), desired)