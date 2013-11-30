#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import test

def main():
    suites = test.all()
    runner = unittest.TextTestRunner().run(suites)

if __name__ == '__main__':
    main()
