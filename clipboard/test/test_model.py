#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import model
from datetime import datetime

date_format = '%Y-%M-%d'

class TmpModel(model.Model):
    title = model.StringField()
    date = model.DateField(date_format)

class TestModel(unittest.TestCase):
    def setUp(self):
        self.date = datetime.strptime('2013-12-1', date_format)
        self.m = TmpModel(title='test', date=self.date)

    def test_model(self):
        self.assertEqual(self.m.title, 'test')
        self.assertEqual(self.m.date, self.date)

        self.assertIsInstance(self.m._fields['title'], model.StringField)
        self.assertIsInstance(self.m._fields['date'], model.DateField)

    def test_field_to_json(self):
        pass

if __name__ == '__main__':
    unittest.main()
