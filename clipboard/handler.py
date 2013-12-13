#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from model import Entry
from datetime import datetime

class Clipboard(tornado.web.RequestHandler):
    def get(self):
        entries = [e for e in Entry.select().order_by(Entry.date.desc())]
        self.render('clipboard.html', entries=entries)

    def post(self):
        content = self.get_argument('content', None)
        date = datetime.now()
        e = Entry.create(content=content, date=date)
        e.save()
        self.redirect('/clipboard')
