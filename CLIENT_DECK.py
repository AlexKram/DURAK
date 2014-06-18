#!/usr/bin/python

import socket
import time
import simplejson
import sys

HOST = '127.0.0.1'    # The remote host
PORT = 5005              # The same port as used by the server
secret_id="secret_deck"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))



def msg_server(func='get_tasks',params=[]):
	msg={
		'func':func,
		'params':params,
		'secret_id': secret_id,
	}
	msg=simplejson.dumps(msg)
	s.send("%04d"%len(msg)+msg)

	size=int(s.recv(4))
	msg=simplejson.loads(s.recv(size))
	print msg
	if msg.has_key('error'):
		raise Exception(msg['error'])
	return msg['return']



from PCDECK import DECK

def convert_card(x):
	if type(x)==type(None):
		return None
	return {
		'suit':x.get_suit(),
		'rank':x.get_rank(),
		'trump':x.is_trump()
	}


init_players=set(['bot1','bot2'])

while 1:
	for x in msg_server('get_tasks'):
		if x=="init_done":
			deck=DECK()
			deck.shuffle()
			print msg_server('init_done',[convert_card(deck.trump_card)])
			break;
		if x=="set_card":
			print msg_server('set_card',[convert_card(deck.get_card())])
			break;
		if x=="set_players":
			names=set([m[0] for m in msg_server('get_players').keys()])
			if len(init_players-names)==0:
				print msg_server('set_players',[list(init_players)])
			break;




	time.sleep(0.1)

s.close()
