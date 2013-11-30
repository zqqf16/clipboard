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

class FieldDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self.field
        return instance._data.get(self.field.name)

    def __set__(self, instance, value):
        instance._data[self.field.name] = value

class Field(object):
    name = ''
    def to_json(self, value):
        return value

class StringField(Field):
    pass

class DateField(Field):
    def __init__(self, format='%Y-%m-%d'):
        self.format = format

    def to_json(self, value):
        if not isinstance(value, datetime):
            raise TypeError('expect {}, got {}'.format('datetime', type(value)))
        return value.strftime(self.format)

class Meta(type):
    def __new__(self, name, bases, attrs):
        _fields = dict((k, v) for k, v in attrs.items() if isinstance(v, Field))

        for k, v in _fields.items():
            v.name = k
            attrs[k] = FieldDescriptor(v)

        attrs['_fields'] = _fields
        attrs['_data'] = {}

        return super(Meta, self).__new__(self, name, bases, attrs)

class Model(object):
    __metaclass__ = Meta
    db = None
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

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
