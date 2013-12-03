#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os

import model
from datetime import datetime

date_format = '%Y-%M-%d'

class TmpModel(model.Model):
    db = model.DataBase('tmp.json')
    title = model.StringField()
    date = model.DateField(date_format)

    def __repr__(self):
        return 'title {}, date {}'.format(self.title, self.date.strftime('%Y-%m-%d'))

class TestModel(unittest.TestCase):
    def setUp(self):
        self.date = datetime.strptime('2013-12-01', date_format)
        self.m = TmpModel(title='test', date=self.date)

    def test_field(self):
        self.assertEqual(self.m.title, 'test')
        self.assertEqual(self.m.date, self.date)

        self.assertIsInstance(self.m._fields['title'], model.StringField)
        self.assertIsInstance(self.m._fields['date'], model.DateField)

        #type
        def set_date(v):
            self.m.date = v

        def set_title(v):
            self.m.title = v

        self.assertRaises(TypeError, set_date, 'string')
        self.assertRaises(TypeError, set_title, self.date)

    def test_field_dump(self):
        d = self.m.dump()
        self.assertEqual(d['date'], '2013-12-01')
        self.assertEqual(d['title'], 'test')

    def test_model_init(self):
        d = self.m.dump()

        m1 = TmpModel(**d)

        self.assertEqual(self.m.date, m1.date)
        self.assertEqual(self.m.title, m1.title)

    def test_save(self):
        t = TmpModel(title="temp", date=datetime.now())
        t2 = TmpModel(title="temp2", date=datetime.now())

        TmpModel.add(t)
        TmpModel.add(t2)
        TmpModel.save()

        a = TmpModel.all()

        self.assertEqual(t.title, a[0].title)
        self.assertEqual(t2.title, a[1].title)
        
        self.clear()

    def clear(self):
        os.remove('tmp.json')

if __name__ == '__main__':
    unittest.main()
