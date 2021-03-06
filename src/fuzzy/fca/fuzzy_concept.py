from fuzzy.FuzzySet import FuzzySet
class FuzzyConcept:
	def __init__(self, extent = FuzzySet(), intent = FuzzySet()):
		self.extent = extent
		self.intent = intent
		
	def __eq__(self, other):
		return self.intent == other.intent and self.extent == other.extent
	
	def __ne__(self, other):
		return not self.__eq__(other)
		
	def __str__(self):
		return str({'intent':self.intent, 'extent':self.extent})
	
	def __hash__(self):
#		return hash(frozenset(self.intent.items())) #^ hash(str(self.extent))
		return hash(self.intent) ^ hash(self.extent)
	
	def __repr__(self):
		return self.__str__()