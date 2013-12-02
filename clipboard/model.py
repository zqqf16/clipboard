#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import uuid
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
        '''Get data from json file'''

        with open(self.name, 'r') as f:
            data = f.read().decode('utf-8')
            if data:
                return json.loads(data)
            else:
                return []

    def save(self, data):
        '''Save given data to json file'''

        with open(self.name, 'w') as f:
            json.dump(data, f)

class Field(object):
    name = ''
    _type = None

    def dump(self, value):
        '''Convert value to a json friendly type'''

        return value

    def load(self, value):
        '''Convert value to "self._type" type'''

        return value

class StringField(Field):
    _type = (str, unicode)

class DateField(Field):
    _type = datetime
    def __init__(self, format='%Y-%m-%d'):
        self.format = format

    def dump(self, value):
        return value.strftime(self.format)

    def load(self, string):
        return datetime.strptime(string, self.format)

class FieldDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self.field
        return instance._data.get(self.field.name)

    def __set__(self, instance, value):
        if not isinstance(value, self.field._type):
            raise TypeError('Error type: {}'.format(type(value)))
        instance._data[self.field.name] = value

class ModelMeta(type):
    def __new__(self, name, bases, attrs):
        _fields = dict((k, v) for k, v in attrs.items() if isinstance(v, Field))

        for k, v in _fields.items():
            v.name = k
            attrs[k] = FieldDescriptor(v)

        attrs['_fields'] = _fields
        attrs['_data'] = {}

        return super(ModelMeta, self).__new__(self, name, bases, attrs)

class Model(object):
    __metaclass__ = ModelMeta
    db = None

    def __init__(self, *args, **kwargs):
        self.id = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def all(cls):
        if not cls.db:
            return []
        return [cls().load(**v) for v in cls.db.get()]

    @classmethod
    def append(cls, instance):
        a = cls.all()
        a.append(instance)
        cls.db.save([i.dump() for i in a])

    def dump(self):
        '''Dump values to json friendly structure'''

        if not self.id:
            #Generate a new id.
            self.id = str(uuid.uuid1())

        _dict = {'id': self.id}

        for column, field in self._fields.items():
            _dict[column] = field.dump(self._data[column])

        return _dict

    def load(self, **kwargs):
        '''Load values from json friendly structure'''

        if kwargs.get('id'):
            self.id = kwargs.get('id')

        for k, v in kwargs.items():
            field = self._fields.get(k, None)
            if not field: continue

            setattr(self, k, field.load(v))

        return self

class Message(Model):
    content = StringField()
    date = DateField()
    db = DataBase('message.json')
