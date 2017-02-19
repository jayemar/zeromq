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

sock.connect('tcp://localhost:' + str(port))

message = sock.recv()
sock.send(b'Rgr from server')

