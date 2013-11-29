#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

FILE_NAME = 'messages.json'

class DataBase(object):
    def __init__(self, name):
        self.name = name

        if not os.path.isfile(self.name):
            with open(self.name, 'w'):
                pass

    def get(self):
        with open(self.name, 'r') as f:
            data = f.read()
            if data:
                return json.load(data)
            else:
                return []

    def save(self, data):
        with open(self.name, 'w') as f:
            json.dump(data, f)

class Field(object):
    name = ''
    _type = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._data.get(self.name, None)

    def __set__(self, instance, value):
        if not isinstance(value, self._type):
            raise TypeError('Type Error')
        instance._data[self.name] = value

class StringField(Field):
    _type = str

class DateField(Field):
    _type = datetime

class Meta(type):
    def __new__(self, name, bases, attrs):
        _fields = tuple((k, v) for k, v in attrs.items() if isinstance(v, Field))

        for k, v in _fields:
            print k, v
            attrs[k].name = k

        return super(Meta, self).__new__(self, name, bases, attrs)

class Model(object):
    __metaclass__ = Meta
    db = None
    def __init__(self):
        self._data = {}

    @classmethod
    def all(cls):
        if not cls.db:
            return []
        return cls.db.get()

    @classmethod
    def append(cls, instance):
        if not cls.db:
            return
        a = cls.db.get()
        a.append(instance._data)
        cls.db.save(a)

class Message(Model):
    content = StringField()
    date = DateField()
    db = DataBase('message.json')
