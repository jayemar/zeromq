#!/usr/bin/env python

import mock
import sys
import unittest
import zmq

class TestPub(unittest.TestCase):

    def setUp(self):
        print("Inside setUp")

    def set_up(self):
        print("Inside set_up")

    def test_setup(self):
        ctx = zmq.Context()
        sock = ctx.socket(zmq.PUB)
        sock.bind('tcp://*:8888')

        assert isinstance(ctx, zmq.Context)
        assert isinstance(sock, zmq.Socket)
