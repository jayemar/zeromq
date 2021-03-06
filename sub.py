#!/usr/bin/env python

import sys
import zmq


class Subscriber(object):
    def __init__(self, context, callback, ip='localhost', port=8888):
        try:
            int(port)
        except ValueError:
            print("Port number must be an integer")
            sys.exit(1)

        try:
            self.ctx = context
            self.callback = callback
            self.sock = context.socket(zmq.SUB)
            print('Connecting to tcp://' + ip + ':' + str(port))
            self.sock.setsockopt(zmq.SUBSCRIBE, bytes('Thing1', encoding='utf-8'))
            self.sock.connect('tcp://' + ip + ':' + str(port))
        except Exception as err:
            raise

    def listen(self):
        while True:
            try:
                [address, msg] = self.sock.recv_multipart()
                self.callback(msg)
            except KeyboardInterrupt:
                self.die()
                print('\r')
                break

    def die(self):
        self.sock.close()
        self.ct.term()
        self.ctx.destroy()


def print_test(msg):
    sys.stdout.buffer.write(bytes("Message received: ", encoding='ascii')
            + msg + bytes("\n", encoding='ascii'))
    sys.stdout.buffer.flush()


if __name__ == '__main__':
    ctx = zmq.Context.instance()
    sub = Subscriber(ctx, print_test)
    sub.listen()

