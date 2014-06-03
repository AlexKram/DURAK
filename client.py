#!/usr/bin/python

import socket
import time
import simplejson
import sys

HOST = '127.0.0.1'    # The remote host
PORT = 5005              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

secret_id="secret_deck"

msg={
	'func':'init_done',
	'params':['asdasd'],
	'secret_id':secret_id,
}
msg=simplejson.dumps(msg)
s.send("%04d"%len(msg)+msg)

size=int(s.recv(4))
msg=simplejson.loads(s.recv(size))
print msg


while 1:
	msg={
		'func':'get_tasks',
		'params':[],
		'secret_id': secret_id,
	}
	msg=simplejson.dumps(msg)
	s.send("%04d"%len(msg)+msg)

	size=int(s.recv(4))
	msg=simplejson.loads(s.recv(size))
	print msg

	time.sleep(0.1)
s.close()
print 'Received', repr(data)
print '---------'
