#!/usr/bin/python

import socket
import time
import simplejson

HOST = '127.0.0.1'    # The remote host
PORT = 5005              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while 1:
	msg={
		'func':'get_id',
		'params':['artur1'],
	}
	msg=simplejson.dumps(msg)
	s.send("%04d"%len(msg)+msg)
	print s.recv(1024)
	time.sleep(5)
s.close()
print 'Received', repr(data)
print '---------'
