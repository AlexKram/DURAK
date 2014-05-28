#!/usr/bin/python


SUITS={
	0:'CLUBS',
	1:'SPADES',
	2:'HEARTS',
	3:'DIAMONDS',
}

RANKS={
	6:'SIX',
	7:'SEVEN',
	8:'EIGHT',
	9:'NINE',
	10:'TEN',
	11:'JACK',
	12:'QUEEN',
	13:'KING',
	14:'ACE',
}


class CARD():
	def __init__(self,suit,rank):
		self.suit=suit
		self.rank=rank
		self.trump=False
	#DECK FUNCTIONS
	def _set_trump_(self):
		self.trump=True
	#other FUNCTION
	def is_trump(self):
		return self.trump
	def get_suit(self):
		return self.suit
	def get_rank(self):
		return self.rank
	def __gt__(self,a):
		return (self.get_rank()<a.get_rank() and self.get_suit()==a.get_suit()) or \
		(not a.is_trump() and self.is_trump())
	
	def __unicode__(self):
		return "%s-%s"%(RANKS[self.get_rank()],SUITS[self.get_suit()])
	def __str__(self):
		return self.__unicode__()
	def __repr__(self):
		return self.__unicode__()
		
		

class DECK():
	def __init__(self):
		self.deck=[]
	def shuffle(self):
		self.deck=[CARD(suit,rank) for rank in RANKS.keys() for suit in SUITS.keys()]	
		import random
		deck=random.shuffle(self.deck)
		for card in self.deck:
			if self.deck[0].get_suit()==card.get_suit():
				card._set_trump_()
	def get_card(self):
		return self.deck.pop()
	def __unicode__(self):
		return "\n".join(map(str,self.deck))
	def __str__(self):
		return self.__unicode__()
	def __repr__(self):
		return self.__unicode__()
		
