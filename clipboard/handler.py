#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from model import Message, datetime

class Clipboard(tornado.web.RequestHandler):
    def get(self):
        msgs = Message.all()
        self.render('clipboard.html', messages=msgs)

    def post(self):
        content = self.get_argument('content', None)
        date = datetime.now()
        m = Message(content=content, date=date)

        Message.add(m)
        Message.save()

        self.redirect('/clipboard')
