#!/usr/bin/python


from pcdeck import DECK
#from worlddeck import DECK

from durak_rules import GAME
#from skat_rules import GAME

from bot1 import PLAYER as PLAYER1
#from bot2 import PLAYER as PLAYER2


deck=DECK()
deck.shuffle()

game=GAME()


players=[PLAYER1(deck,game),PLAYER1(deck,game)]

import time
while True:
	for p in players:
		p.do_work()	




print deck




