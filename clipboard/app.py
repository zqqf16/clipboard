#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import tornado.ioloop
import tornado.web
import tornado.httpserver

from handler import Clipboard

class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', Clipboard),
            (r'/clipboard', Clipboard)
        ]

        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
        }

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

