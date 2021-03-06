#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 update usage in one year
"""
__author__ = 'Xu, Yuan'

from day import mergeAppDataList, updateCategory
from month import Month


class Year():
    def __init__(self, year):
        self.applicationList = []
        self.categoryList = []
        for i in range(1, 13):
            result = Month(year, i)
            self.applicationList = mergeAppDataList(self.applicationList,
                                                    result.applicationList)
        self.categoryList = updateCategory(self.applicationList)
        self.applicationList.sort()
        self.categoryList.sort()
        self.info = "%(year)d" % vars()