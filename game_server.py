#!/usr/bin/python


import socket
import select
import time
import simplejson
import pprint
import random
import uuid


TIMEOUT=2000
class MEMBER():
	def __init__(self,name):
		self.name=name
		self.secret_id=str(uuid.uuid1())
		self.last_time=time.time()
	def get_secret_id(self):
		return self.secret_id
	def check_timeout(self):
		return time.time()-self.last_time>TIMEOUT
	def get_mode(self):
		return self.mode
	def get_mode(self):
		return "MEMBER"

class MASTER():
	def __init__(self):
		self.secret_id=str(uuid.uuid1())
	def get_secret_id(self):
		return self.secret_id
	def get_mode(self):
		return "MASTER"

class DECK():
	def __init__(self):
		self.secret_id="secret_deck"
		self.card=None
		self.deck_clean=False
		self.init=False
	def get_secret_id(self):
		return self.secret_id
	def get_mode(self):
		return "DECK"
	def get_card(self):
		if self.deck_clean:
			raise Exception("No card on stack")
		tmpcard=self.card
		self.card=None
		return tmpcard
	def ext_set_card(self,card):
		self.card=card
	def ext_empty_deck(self):
		self.deck_clean=True
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
class WORKER():
	def __init__(self):
		self.members={}
		self.master=MASTER()
		self.deck=DECK()
		print "Master: ",self.master.get_secret_id()
		print "Deck: ",self.deck.get_secret_id()

	def ext_get_id(self,name):
		if len(self.members.keys())>MAX_MEMBERS:
			return {'error': 'To much Members'}
		m=MEMBER(name)
		self.members[m.get_secret_id()]=m
		return {'return':m.get_secret_id()}
	
	def ext_get_card(self,member):
		#XXX
		#TODO check valid order for getting a card
		try:
			card = self.deck.get_card()
			if card:
				return {'return': card}
			return {'error': "please try again"}
		except:
			return {'return': None}
		
		

	def msg_work(self,msg):

		func=msg.setdefault('func','get_task')
		print func

		#NEW member
		if func=='get_id':
			try:
				return self.ext_get_id(*msg['params'])
			except:
				return {'error': 'bullshit'}


		#find unknown client	
		try:
			secret_id=msg['secret_id']
		except:
			return {'error':'No secret_id given'}
		
		member=None
		if secret_id==self.master.get_secret_id():
			member=self.master

		if secret_id==self.deck.get_secret_id():
			member=self.deck

		if not member:
			try:
				member=self.members[secret_id]
			except:
				return {'error':'No such member'}
		
		try:	
			return getattr(self,"ext_"+func)(member,*msg['params'])
		except:
			try:
				return getattr(member,"ext_"+func)(*msg['params'])
			except:
				pass
			return {'error': "Wrong params"}
	











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


