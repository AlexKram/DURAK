#!/usr/bin/python
import time

class PLAYER():
	def __init__(self,deck,game,name=None):
		self.deck=deck
		self.game=game
		self.name=name
		self.hand=[]
		self.player_id=None
	def do_work(self):
		for task in self.game.get_tasks(self.player_id):
			getattr(self,task)()
	def register_member(self):
		self.player_id=self.game.register_member()
	def get_card(self):
		self.hand.append(self.deck.get_card())
		self.game.get_card(self.player_id)
	def check_hand(self):
		self.game.check_hand(self.player_id,self.hand)
	def print_status(self):
		print self.hand
		
			
	
