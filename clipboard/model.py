#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from peewee import *

_DB = 'clipboard.db'
db = SqliteDatabase(_DB)

class Entry(Model):
    date = DateTimeField()
    content = TextField()

    class Meta:
        database = db

    def to_dict(self):
        return {'id':self.id, 'date':self.date.strftime('%Y-%m-%d %H:%M'), 'content':self.content}

def init(db_name=_DB):
    if os.path.isfile(db_name):
        return

    #Create table
    Entry.create_table()

if __name__ == '__main__':
    init()
