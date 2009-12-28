#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 update usage in one year
"""
__author__ = 'Xu, Yuan'

from month import Month

class Year():
    def __init__(self, year):
        self.applicationList = []
        self.categoryList = []
        for i in range(1, 12):
            result = Month(year, i)
            self.applicationList += result.applicationList
            self.categoryList += result.categoryList
        self.info = "%(year)d" % vars()
