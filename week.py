#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 update weekly usage
"""
__author__ = 'Xu, Yuan'

import datetime
from day import Day, mergeAppDataList, mergeCateoryList

class Week():
    def __init__(self, year, month, day):
        self.applicationList = []
        self.categoryList = []
        d = datetime.date.today()
        if day is not 0:
            d = datetime.date(year, month, day)
        d = d + datetime.timedelta(days=-d.weekday())
        for i in range(0,6):
            theday = d + datetime.timedelta(days=i)
            result = Day(theday.year, theday.month, theday.day)
            self.applicationList = mergeAppDataList(self.applicationList, result.applicationList)
            self.categoryList = mergeCateoryList(self.categoryList, result.categoryList)
        self.info = d.isoformat() + " ~ " + (d+datetime.timedelta(days=7)).isoformat()

