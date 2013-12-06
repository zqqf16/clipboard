#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import uuid
import os
from datetime import datetime

class DataBase(object):
    def __init__(self, name):
        self.name = name

        if not os.path.isfile(self.name):
            print "not file"
            with open(self.name, 'w'):
                pass

    def read(self):
        '''Get data from json file'''

        with open(self.name, 'r') as f:
            data = f.read().decode('utf-8')
            if data:
                return json.loads(data)
            else:
                return []

    def write(self, data):
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
    def __init__(self, format='%Y-%m-%d %H:%M'):
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

        if not hasattr(instance, '_data'):
            setattr(instance, '_data', {})

        return instance._data.get(self.field.name)

    def __set__(self, instance, value):
        if not isinstance(value, self.field._type):
            raise TypeError('Error type: {}'.format(type(value)))

        if not hasattr(instance, '_data'):
            setattr(instance, '_data', {})

        instance._data[self.field.name] = value

class ModelMeta(type):
    def __new__(self, name, bases, attrs):
        _fields = dict((k, v) for k, v in attrs.items() if isinstance(v, Field))

        for k, v in _fields.items():
            v.name = k
            attrs[k] = FieldDescriptor(v)

        attrs['_fields'] = _fields

        return super(ModelMeta, self).__new__(self, name, bases, attrs)

class Model(object):
    __metaclass__ = ModelMeta
    db = None
    _all = None

    def __init__(self, id=None, **kwargs):
        if id:
            # load from database
            for k, v in kwargs.items():
                field = self._fields.get(k, None)
                if not field: continue
                setattr(self, k, field.load(v))
        else:
            for k, v in kwargs.items():
                setattr(self, k, v)
        
        self.id = id if id else str(uuid.uuid1())

    @classmethod
    def all(cls):
        if cls._all != None:
            return cls._all

        if cls.db:
            jsons = cls.db.read()
            cls._all = [cls(**j) for j in jsons]
        else:
            cls._all = []

        return cls._all

    @classmethod
    def add(cls, m):
        if cls._all != None:
            for c in cls._all:
                if c.id == m.id:
                    return
            cls._all.append(m)
        else:
            cls._all = [m]

    @classmethod
    def delete(cls, m):
        pass

    @classmethod
    def save(cls):
        if cls._all == None:
            return

        if not cls.db:
            return

        cls.db.write([m.dump() for m in cls._all])

    def dump(self):
        '''Dump values to json friendly structure'''

        _dict = {'id': self.id}

        for column, field in self._fields.items():
            _dict[column] = field.dump(self._data[column])

        return _dict

class Message(Model):
    content = StringField()
    date = DateField()
    db = DataBase('message.json')
