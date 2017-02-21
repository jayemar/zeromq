#!/usr/bin/env python

import sys
import threading
import time
import zmq
from zmq.error import ZMQError
from pprint import pprint as pp


class Publisher(object):
    def __init__(self, context, port=8888):
        # Make sure the requested port number is valid
        try:
            int(port)
            self.port = str(port)
            self.status_port = str(int(port) + 1)
        except ValueError:
            print("Port number must be an integer")
            sys.exit(1)

        self.ctx = context

        # Create thread to listen for new requests
        status_thread = threading.Thread(target=self.status_manager,
                args=('yes', 'sir'))
        status_thread.daemon = True
        status_thread.start()

        # Create pub socket
        try:
            self.sock = context.socket(zmq.PUB)
            print('Connecting to tcp://*:' + self.port)
            self.sock.bind('tcp://*:' + self.port)
        except Exception as err:
            raise

    def send_msg(self, msg, address='default_address'):
        self.sock.send_multipart([bytes(address, encoding='utf-8'),
                bytes(msg, encoding='utf-8')])

    def die(self):
        self.sock.close()
        self.ctx.term()
        self.ctx.destroy()

    def status_manager(self, b, c):
        self.status = self.ctx.socket(zmq.REP)
        print('Connecting Status Manager to tcp://*:' + self.status_port)
        self.status.bind('tcp://*:' + self.status_port)
        while True:
            msg = self.status.recv()
            #print('Message received by Status Manager')
            pp(self._get_status_dict())
            self.status.send(b'Message received')

    def _get_status_dict(self):
        status = {'status': 'OK'}
        status['twsec'], status['tfsec'] = time.time().__repr__().split('.')
        return status

if __name__ == '__main__':
    ctx = zmq.Context.instance()
    pub = Publisher(ctx)
    while True:
        try:
            time.sleep(5.0)
            print("Sending message 'Hello World'")
            pub.send_msg("Hello World", 'Thing1')
        except KeyboardInterrupt:
            pub.die()
            print('\r')
            break

