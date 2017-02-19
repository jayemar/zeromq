#!/usr/bin/env python

import sys
import zmq
from zmq.error import ZMQError

def handle_reply(msg):
    print("Reply received")

try:
    port = int(sys.argv[1])
except IndexError:
    port = 8888
except ValueError:
    print("ERROR: The port number must be an integer")
    sys.exit(1)

context = zmq.Context()
sock = context.socket(zmq.REP)

print('Attempting to bind to tcp://*:' + str(port))
try:
    sock.bind('tcp://*:' + str(port))
except ZMQError as err:
    print("Error binding socket: %s" % err)
    sock.close()
    context.destroy()

message = sock.recv()
print("Received message from client: %s" % str(message))
print("Sending reply")
sock.send(b'Rgr from server')
sock.close()
context.destroy()

