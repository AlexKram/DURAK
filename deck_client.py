#!/usr/bin/python

import socket
import time
import simplejson
import random
import hmac
import sys

HOST = '127.0.0.1'    # The remote host
PORT = 5005              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


secret_id=sys.argv[1]



from pcdeck import DECK



def set_card():
	obj_card=deck.get_card()
	if obj_card==None:
		msg={
			'func':'empty_deck',
			'params':[],
			'secret_id':secret_id,
		}
	else:
		card={
			'suit': obj_card.get_suit(),
			'rank': obj_card.get_rank(),
			'trump': obj_card.is_trump(),
		}
		card['sign']=hmac.new(secret_id,"%02d%02d%02d"%(card['suit'],card['rank'],int(card['trump']))).hexdigest()
		msg={
			'func':'set_card',
			'params':[card],
			'secret_id':secret_id,
		}
	return msg


while 1:

	msg={
		'func':'get_task',
		'params':[],
		'secret_id':secret_id,
	}

	msg=simplejson.dumps(msg)
	s.send("%04d"%len(msg)+msg)


	size=int(s.recv(4))
	msg=simplejson.loads(s.recv(size))



	if msg['return'] == "set_card":
		omsg=set_card()
		omsg=simplejson.dumps(omsg)
		s.send("%04d"%len(omsg)+omsg)
		size=int(s.recv(4))
		omsg=simplejson.loads(s.recv(size))
	if msg['return'] == 'check_card':
		card=msg['card']
		sign=hmac.new(secret_id,"%02d%02d%02d"%(card['suit'],card['rank'],int(card['trump']))).hexdigest()
		if sign==card['sign']:
			omsg={
				'func':'card_valid',
				'params':[],
				'secret_id':secret_id,
			}
		else:
			omsg={
				'func':'card_invalid',
				'params':[],
				'secret_id':secret_id,
			}
		omsg=simplejson.dumps(omsg)
		s.send("%04d"%len(omsg)+omsg)
		size=int(s.recv(4))
		omsg=simplejson.loads(s.recv(size))
	if msg['return'] == "init":
		deck=DECK()
		deck.shuffle()
		omsg={
			'func':'init',
			'params':[],
			'secret_id':secret_id,
		}
		omsg=simplejson.dumps(omsg)
		s.send("%04d"%len(omsg)+omsg)
		size=int(s.recv(4))
		omsg=simplejson.loads(s.recv(size))

		
		

	time.sleep(0.2)
s.close()
print 'Received', repr(data)
print '---------'
