#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

ALL_MODULES = [
    'test.test_web',
]

def all():
    return unittest.defaultTestLoader.loadTestsFromNames(ALL_MODULES)
