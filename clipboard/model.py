#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from peewee import *

_DB = 'clipboard.db'
db = SqliteDatabase(_DB)

class Message(Model):
    date = DateTimeField()
    content = TextField()

    class Meta:
        database = db

def init(db_name=_DB):
    if os.path.isfile(db_name):
        return

    #Create table
    Message.create_table()

if __name__ == '__main__':
    init()
