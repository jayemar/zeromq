#!/usr/bin/env python

import sys
import zmq

def handle_reply(msg):
    print("Reply received")

try:
    port = int(sys.argv[1])
except IndexError:
    port = 8888
except ValueError:
    print("ERROR: The port number must be in integer")
    sys.exit(1)

context = zmq.Context.instance()
sock = context.socket(zmq.REQ)
sock.linger = 0

print('Connecting to tcp://localhost:' + str(port))
sock.connect('tcp://localhost:' + str(port))

print("Sending message to server")
sock.send(bytes('Client message', encoding='ascii'))
response = sock.recv()
print("Response from Server: %s" % response)

