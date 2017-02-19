#!/usr/bin/env python

import sys
import time
import zmq
from zmq.error import ZMQError


class Publisher(object):
    def __init__(self, context, port=8888):
        try:
            int(port)
        except ValueError:
            print("Port number must be an integer")
            sys.exit(1)

        try:
            self.ctx = context
            self.sock = context.socket(zmq.PUB)
            print('Connecting to tcp://*:' + str(port))
            self.sock.bind('tcp://*:' + str(port))
        except Exception as err:
            raise

    def send(self, msg):
        self.sock.send_string(msg)

    def die(self):
        self.sock.close()
        self.ctx.destroy()

if __name__ == '__main__':
    ctx = zmq.Context.instance()
    pub = Publisher(ctx)
    while True:
        try:
            time.sleep(1.0)
            print("Sending message 'Hello World'")
            pub.send("Hello World")
        except KeyboardInterrupt:
            pub.die()
            print('\r')
            break

