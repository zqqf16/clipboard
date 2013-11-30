#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

class Clipboard(tornado.web.RequestHandler):
    def get(self):
        self.render('clipboard.html')

    def post(self):
        print self.get_argument('content', None)
