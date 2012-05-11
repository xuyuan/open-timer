#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 update daily usage
"""
__author__ = 'Xu, Yuan'

import re
import time
import os

from dict import appdict, categoryDict


class Application():
    def __init__(self, n, s):
        self.name = n
        self.p = re.compile(s)
        self.count = 0
        self.t = 0

    def match(self, s):
        if self.p.match(s):
            self.count += 1
            return True
        else:
            return False

    def addTime(self, t):
        self.t += t

    def __cmp__(self, other):
        return other.time() - self.time()

    def time(self):
        return self.t


def createListFromDict(type, sd):
    pl = []
    for x in sd.keys():
        pl.append(type(x, sd[x]))
    return pl


def removeZeroTime(l):
    r = []
    for e in l:
        if e.time() > 0:
            r.append(e)
    return r


def mergeAppDataList(la, lb):
    for v in lb:
        merge = False
        for va in la:
            if v.name == va.name:
                va.count += v.count
                va.t += v.t
                merge = True
                break
        if merge is False:
            la.append(v)
    return la


class Category():
    """
    Application category according to its function
    """
    def __init__(self, n, s):
        self.name = n
        self.p = re.compile(s)
        self.apps = []

    def match(self, app):
        for a in self.apps:
            if a.name == app.name:
                a.addTime(app.time())
                return True

        if self.p.match(app.name):
            self.apps.append(app)
            return True
        else:
            return False

    def time(self):
        t = 0
        for a in self.apps:
            t += a.time()
        return t

    def __cmp__(self, other):
        return other.time() - self.time()


def updateCategory(applist):
    categoryList = createListFromDict(Category, categoryDict)
    other = Category('Uncategorized', '.')
    for app in applist:
        ismatched = False
        for c in categoryList:
            if c.match(app):
                ismatched = True
                break
        if not ismatched:
            other.match(app)

        # print other.name, ':'
        # for o in other.apps:
           # print o.name, o.time()

    categoryList = removeZeroTime(categoryList)
    categoryList.sort()
    if other.time() > 0:
        categoryList.append(other)

    return categoryList


class Day():
    def __init__(self, year=0, month=0, day=0):
        if day == 0:
            self.info = time.strftime('%Y-%m-%d', time.localtime())
            self.filename = time.strftime('%Y/%m/%d.txt', time.localtime())
        else:
            self.info = '%(year)d-%(month).2d-%(day).2d' % vars()
            self.filename = '%(year)d/%(month).2d/%(day).2d.txt' % vars()
        self.filename = os.path.join(os.path.dirname(__file__),
                                    'data', self.filename)
        self.update()

    def updateApp(self, printunkown=True, checkcollision=False):
        pstart = Application('start', '^start')
        pstop = Application('stop', '^stop')
        other = Application('other', '.')

        applist = createListFromDict(Application, appdict)

        try:
            f = open(self.filename, 'r')
            line = f.readline()
            ln = 1
            laststs = None
            lastmatched = pstart
            while len(line) > 0:
                pmatched = None
            #print line,
                st = laststs
                try:
                    if pstart.match(line):
                        st = time.strptime(line[6:14], "%H:%M:%S")
                        pmatched = pstart
                        laststs = (st.tm_hour * 3600
                                    + st.tm_min * 60 + st.tm_sec)
                    elif pstop.match(line):
                        st = time.strptime(line[5:13], "%H:%M:%S")
                        pmatched = pstop
                        sts = st.tm_hour * 3600 + st.tm_min * 60 + st.tm_sec
                        dt = sts - laststs
                        lastmatched.addTime(dt)
                        laststs = sts
                    else:
                        ismatched = False
                        title = line[9:]
                        st = time.strptime(line[:8], "%H:%M:%S")
                        sts = st.tm_hour * 3600 + st.tm_min * 60 + st.tm_sec
                        dt = sts - laststs
                        lastmatched.addTime(dt)
                        for a in applist:
                            if a.match(title):
                                if checkcollision and ismatched:
                                    print ('App collision!!!',
                                            pmatched.name, ' : ', a.name)
                                    print line
                                pmatched = a
                                ismatched = True
                                if not checkcollision:
                                    break
                        if not ismatched:
                            if printunkown:
                                print line.decode('utf-8'),
                            other.match(title)
                            pmatched = other

                        laststs = sts
                        lastmatched = pmatched
                except ValueError:
                        print 'ValueError @ ' + self.filename + ' %d' % ln
                        print "'" + line + "'"

                line = f.readline()
                ln = ln + 1

        except IOError:
            self.info += ' data is empty'

        applist = removeZeroTime(applist)
        if other.time() > 0:
            applist.append(other)
        applist.sort()

            #print
            #print
            #for p in patternlist:
            #    print p.name, p.count, p.time/60.0

        return applist

    def update(self):
        self.applicationList = self.updateApp()
        self.categoryList = updateCategory(self.applicationList)