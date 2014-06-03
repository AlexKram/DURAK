#!/usr/bin/python


import socket
import select
import time
import simplejson
import pprint
import random
import uuid



class MEMBER():
	def __init__(self,name):
		self._name_=name
		self._secret_id_=str(uuid.uuid1())
		self._num_of_cards_=0
		self._position_=None
	@property
	def name(self):
		return self._name_
	@property
	def secret_id(self):
		return self._secret_id_
	@property
	def num_of_cards(self):
		return self._num_of_cards_
	@num_of_cards.setter
	def num_of_cards(self,value):
		self._num_of_cards_=value
	@property
	def position(self):
		return self._position_
	@position.setter
	def position(self,value):
		self._position_=value

class DECK():
	def __init__(self):
		self._secret_id_="secret_deck"
		self._card_=None
		self._deck_empty_=False
		self._trump_card_=None
	@property
	def secret_id(self):
		return self._secret_id_
	@property
	def trump_card(self):
		return self._trump_card_
	@trump_card.setter
	def trump_card(self, value):
		self._trump_card_=value
	@property
	def card(self):
		if self.deck_empty:
			raise Exception("No card on stack")
		tmp_card=self._card_
		self._card_=None
		return tmp_card
	@card.setter
	def card(self,value):
		self._card_=value
	@property
	def deck_empty(self):
		return self._deck_empty_
	@deck_empty.setter
	def deck_empty(self,value):
		self._deck_empty_=value
	def ext_get_task(self):
		if not self.init:
			return {'return': 'init'}
		if self.card==None:
			return {'return': 'set_card'}
		return {'return': 'none'}
	def ext_init(self):
		self.init=True
		return {}



MAX_MEMBERS=5

#STATES
STATE_INIT	=2**0
STATE_REGISTER	=2**1
STATE_RAISE_HAND=2**2
STATE_UNKNOWN	=2**3
STATE_ALL_ABOVE=2**17-1

STATE_NEED_MEMBER=2**18
STATE_DECK_MEMBER=2**19


def deco(state):
	def STATER(func):
		def real_func(self,*args,**kwargs):
			if self.STATE&state:
				if STATE_NEED_MEMBER&state and kwargs['member']==None:
					return {'error': "No Member"}
				if STATE_DECK_MEMBER&state and not hasattr(kwargs['member'],'card'):
					return {'error': "No Deck Member"}
				try:
					ret=func(self,*args,**kwargs)
				except None:
					ret = {'error': "PYTHON EXCEPTION"}
				return ret
			return {'error': "Invalid state"}
		return real_func
	return STATER

class WORKER():

	def __init__(self):
		self.members={}
		self.deck=DECK()
		self.player_on_turn=None
		self.STATE=STATE_INIT

	@deco(STATE_ALL_ABOVE)
	def ext_get_tasks(self,member=None):
		if member==None:
			return {'return':['get_tasks','get_trump_card']}
		if hasattr(member,'card'):
			ret=['get_tasks','get_trump_card']
			if self.STATE==STATE_INIT:
				ret=['init_done']+ret
			if self.STATE==STATE_REGISTER:
				ret=['get_players','set_players']+ret
			if self.STATE==STATE_RAISE_HAND and self.deck._card_==None:
				ret=['set_card']+ret
			return ret
		return member.ext_get_tasks()

	@deco(STATE_INIT|STATE_DECK_MEMBER)
	def ext_init_done(self,trump_card,member=None):
		print "INIT"
		self.members={}
		self.deck=DECK()
		self.player_on_turn=None
		self.deck.trump_card=trump_card
		self.STATE=STATE_REGISTER
		return {'return': 'Initialisation successfull!'}


	def msg_work(self,msg):
		if type(msg)!=type({}):
			return {'error':'No dict given'}

		func=msg.setdefault('func','get_task')
		secret_id=msg.setdefault('secret_id','bullshit')
		params=msg.setdefault('params',[])

		member=None
		if self.members.has_key(secret_id):
			member=self.members[secret_id]
		if secret_id==self.deck.secret_id:
			member=self.deck

		if hasattr(self,"ext_"+func):
			return getattr(self,"ext_"+func)(*params,member=member)
		else:
			return {'error': "No such function"}


#
#
#
#
#
#	def ext_get_id(self,name):
#		if len(self.members.keys())>MAX_MEMBERS:
#			return {'error': 'To much Members'}
#		if name in [x.name for x in self.members.values()]:
#			return {'error': "Name already in use"}
#		m=MEMBER(name)
#		self.members[m.get_secret_id()]=m
#		return {'return':m.get_secret_id()}
#	
#	def ext_get_card(self,member):
#		#XXX
#		#TODO check valid order for getting a card
#		(self.player_on_turn or 1) 
#		
#		try:
#			card = self.deck.card
#			if card:
#				member.num_of_cards+=1
#				return {'return': card}
#			return {'error': "please try again"}
#		except:
#			return {'return': None}
#
#
#
#
#
#
#
#
#
#
#		if self.STATE==STATE_INIT:
#			self.members={}
#			self.deck=DECK()
#			self.player_on_turn=None
#			print "Deck: ",self.deck.get_secret_id()
#
#			if secret_id==self.deck.get_secret_id() and func=='init_done':
#				self.deck.trump_card=msg['trump_card']
#				self.STATE=STATE_REGISTER
#				return {'return': 'Initialisation successfull!'}
#			else
#				return {'error': 'bullshit'}
#
#		if self.STATE==STATE_REGISTER:
#			if func=='get_id':
#				try:
#					return self.ext_get_id(*msg['params'])
#				except:
#					return {'error': 'bullshit'}
#			if func=='get_players':
#				return dict([(x.name,x.position) for x in self.members.values()])
#
#			if secret_id==self.deck.get_secret_id() and func=='set_players':
#				msg.setdefault('params',[[]])
#				if len(set([msg['params'][0]))>1 and \
#				   len(set([x.name for x in self.members.values()]) - set(msg['params'][0]))==0:
#					counter=0
#					for x in msg['params'][0]:
#						for m in self.members.values():
#							if m.name==x:
#								m.position=counter
#								counter+=1					
#
#					for x in self.members.keys():
#						if self.members[x].position==None:
#							del self.members[x]
#					self.STATE=STATE_RAISE_HAND
#					return {'return': 'Registration successfull!'}
#				else:
#					return {'error': 'bullshit'}
#		if self.STATE==STATE_RAISE_HAND:
#			if secret_id==self.deck.get_secret_id():
#				if func=="set_card":
#					tmpcard=self.deck.card
#					if tmpcard==None:
#						self.deck.card=msg['params'][0]
#						return {'return': 'ok'}
#					else:
#						self.deck.card=tmpcard
#						return {'error': 'card stack full'}
#				return {'error': 'no such function'}
#			else:
#				try:
#					member=self.members[secret_id]
#				except:
#					return {'error': "Not such member"}
#				if func=="get_card":
#					card=self.get_card(member)
##XXX check next
#					if self.deck.deck_empty or \
#					   len(filter(lambda x: x.num_of_cards>5,self.members.values()))==len(self.members.values()):
#						self.STATE==STATE_UNKNOWN
#					return card
#				else:
#					return {'error': "only get card"}
#
#		if self.STATE==STATE_UNKNOWN:
#			print "Unknown state reached"
#			self.STATE=STATE_INIT
#			
#
#
#		return {}
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#		#NEW member
#		if func=='get_id':
#			try:
#				return self.ext_get_id(*msg['params'])
#			except:
#				return {'error': 'bullshit'}
#
#
#		#find unknown client	
#
#		
#		member=None
#		if secret_id==self.master.get_secret_id():
#			member=self.master
#
#		if secret_id==self.deck.get_secret_id():
#			member=self.deck
#
#		if not member:
#			try:
#				member=self.members[secret_id]
#			except:
#				return {'error':'No such member'}
#		
#		try:	
#			return getattr(self,"ext_"+func)(member,*msg['params'])
#		except:
#			try:
#				return getattr(member,"ext_"+func)(*msg['params'])
#			except:
#				pass
#			return {'error': "Wrong params"}
	











#TCP STREAM WORKER


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 200  # Normally 1024, but we want fast response
MAX_INPUT_BUFFER=4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)
server.bind((TCP_IP, TCP_PORT))
server.listen(5)
 

inputs = {
		server.fileno():["server",server]
}

worker=WORKER()

def parse_msg(buff,client):
	if len(buff)<5:
		return buff
	try:
		size=int(buff[:4])
	except:
		return buff

	if len(buff)<size+4:
		return buff
	try:
		msg=simplejson.loads(buff[4:size+4])
	except:
		return buff
	
	nmsg=worker.msg_work(msg)
	nmsg=simplejson.dumps(nmsg)
	client.send("%04d"%len(nmsg)+nmsg)
	return buff[size+4:]
	

while 1:
	r,w,e = select.select(inputs.keys(), [], inputs.keys(),1.0)
	try:
		r=r[0]

		if inputs[r][0]=='server':
			conn, addr = inputs[r][1].accept()
			inputs[conn.fileno()]=["client",conn,""]
			print "Connection from ",addr

		if inputs[r][0]=='client':
			m=inputs[r][1].recv(BUFFER_SIZE)
			if not m:
				inputs[r][1].close()
				del inputs[r]
			else:
				inputs[r][2]+=m
				inputs[r][2]=inputs[r][2][-1*MAX_INPUT_BUFFER:]
	except:
		pass
	for inp in inputs.values():
		if inp[0]=="client": inp[2]=parse_msg(inp[2],inp[1])
	#print r,w,e,inputs


