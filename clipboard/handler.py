#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from model import Entry
from datetime import datetime
import json

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        entries = [e for e in Entry.select().order_by(Entry.date.desc())]
        self.render('clipboard.html', entries=entries)

    def post(self):
        content = self.get_argument('content', None)
        date = datetime.now()
        e = Entry.create(content=content, date=date)
        e.save()
        self.redirect('/')

#REST api
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        entries = [e.to_dict() for e in Entry.select().order_by(Entry.date.desc())]
        self.write(json.dumps(entries))

    def post(self):
        content = self.get_argument('content', None)
        date = datetime.now()
        e = Entry.create(content=content, date=date)
        e.save()
        self.write({'status':'success'})

class SingleHandler(tornado.web.RequestHandler):
    def get(self, id):
        e = Entry.get(Entry.id == id)
        self.write(e.to_dict())

    def delete(self, id):
        e = Entry.get(Entry.id == id)
        if not e:
            self.write({'status':'error'})
            return

        e.delete_instance()
        self.write({'status':'success'})
