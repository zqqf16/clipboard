#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from model import Message
from datetime import datetime

class Clipboard(tornado.web.RequestHandler):
    def get(self):
        msgs = [m for m in Message.select().order_by(Message.date.desc())]
        msgs.sort(lambda x, y: cmp(x.date, y.date), reverse=True)
        self.render('clipboard.html', messages=msgs)

    def post(self):
        content = self.get_argument('content', None)
        date = datetime.now()
        m = Message.create(content=content, date=date)
        m.save()
        self.redirect('/clipboard')
