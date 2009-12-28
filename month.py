#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 update monthly usage
"""
__author__ = 'Xu, Yuan'

import calendar
from day import Day

class Month():
    def __init__(self, year, month):
        self.applicationList = []
        self.categoryList = []
        r = calendar.monthrange(year, month)
        for i in range(r[0], r[1]):
            result = Day(year, month, i)
            self.applicationList += result.applicationList
            self.categoryList += result.categoryList
        self.info = "%(year)d-%(month)d" % vars()

