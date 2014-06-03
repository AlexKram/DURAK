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






msg_server()
msg_server('init_done',['as'])

while 1:
	msg_server()
	time.sleep(0.1)

s.close()
