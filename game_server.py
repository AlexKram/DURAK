#!/usr/bin/python


import socket
import select
import time
import simplejson
import pprint
import random


TIMEOUT=2000
class MEMBER():
	def __init__(self,name):
		self.name=name
		self.secret_id=random.randint(1,100000)
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
		self.secret_id=random.randint(1,100000)
	def get_secret_id(self):
		return self.secret_id
	def get_mode(self):
		return "MASTER"

class DECK():
	def __init__(self):
		self.secret_id=random.randint(1,100000)
	def get_secret_id(self):
		return self.secret_id
	def get_mode(self):
		return "DECK"

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

	def msg_work(self,msg):

		func=msg.setdefault('func','get_task')

		#NEW member
		if func=='get_id':
			return self.ext_get_id(*msg['params'])


		#find unknown client	
		try:
			secret_id=msg['secret_id']
		except:
			return {'error':'No secret_id given'}

		if secret_id==self.master.get_secret_id():
			member=self.master

		if secret_id==self.deck.get_secret_id():
			member=self.deck

		try:
			member=self.members[secret_id]
	
		return getattr(self,'')
	











#TCP STREAM WORKER


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 200  # Normally 1024, but we want fast response
MAX_INPUT_BUFFER=4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind((TCP_IP, TCP_PORT))
server.listen(5)
 

inputs = {
		server.fileno():["server",server]
}

worker=WORKER()

def parse_msg(buff,client):
	try:
		size=int(buff[:4])
	except:
		return buff
	msg=None
	try:
		msg=simplejson.loads(buff[4:size+4])
	except:
		return buff
	if msg:
		nmsg=worker.msg_work(msg)
		nmsg=simplejson.dumps(nmsg)
		client.send("%04d"%len(nmsg)+nmsg)
	return buff[size+4:]
	

while 1:
	r,w,e = select.select(inputs.keys(), [], inputs.keys(),1.0)
	try:
		r=r[0]
	except:
		pass
	finally:
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
	for inp in inputs.values():
		if inp[0]=="client": inp[2]=parse_msg(inp[2],inp[1])
	#print r,w,e,inputs


