#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 update monthly usage
"""
__author__ = 'Xu, Yuan'

import calendar
from day import Day, mergeAppDataList, updateCategory

class Month():
    def __init__(self, year, month):
        self.applicationList = []
        self.categoryList = []
        r = calendar.monthrange(year, month)
        for i in range(r[0]+1, r[1]+1):
            result = Day(year, month, i)
            self.applicationList = mergeAppDataList(self.applicationList, result.applicationList)
        self.categoryList = updateCategory(self.applicationList)
        self.applicationList.sort()
        self.categoryList.sort()
        self.info = "%(year)d-%(month)d" % vars()

