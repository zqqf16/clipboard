#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import tornado
import tornado.httpclient

import app

class TestModel(unittest.TestCase):
    def setUp(self):
        application = app.App()
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8888)

    def handle_request(self, response):
        self.response = response
        tornado.ioloop.IOLoop.instance().stop()

    def test_get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch('http://0.0.0.0:8888', self.handle_request)
        tornado.ioloop.IOLoop.instance().start()

        print self.response.body


if __name__ == '__main__':
    unittest.main()
