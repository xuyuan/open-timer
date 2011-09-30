#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 update weekly usage
"""
__author__ = 'Xu, Yuan'

import datetime
from day import Day, mergeAppDataList, updateCategory


class Week():
    def __init__(self, year, month, day):
        self.applicationList = []
        self.categoryList = []
        d = datetime.date.today()
        if day is not 0:
            d = datetime.date(year, month, day)
        d = d + datetime.timedelta(days=-d.weekday())
        for i in xrange(7):
            theday = d + datetime.timedelta(days=i)
            result = Day(theday.year, theday.month, theday.day)
            self.applicationList = mergeAppDataList(self.applicationList,
                                                    result.applicationList)
        self.categoryList = updateCategory(self.applicationList)
        self.applicationList.sort()
        self.categoryList.sort()
        self.info = (d.isoformat() + " ~ " +
                    (d + datetime.timedelta(days=7)).isoformat())