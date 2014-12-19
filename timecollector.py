#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
collecting data from your current window's title

Dependence (MS Windows):
 Python Extensions for Windows (http://sourceforge.net/projects/pywin32/)
"""
__author__ = 'Xu, Yuan'

import sys
import time
import os
import platform
import codecs
import threading
import atexit

if platform.system() == 'Windows':
    import win32gui
elif platform.system() == 'Linux':
    import subprocess


def makeSureDir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def checkDataDir():
    datadir = os.path.dirname(os.path.realpath(__file__))
    datadir += "/data"
    makeSureDir(datadir)
    datadir += time.strftime("/%Y", time.localtime())
    makeSureDir(datadir)
    datadir += time.strftime("/%m", time.localtime())
    makeSureDir(datadir)
    return datadir


def hhmmss(t):
        return time.strftime("%H:%M:%S", t)


class TimeCollector():
    def __init__(self):
        self.file = None
        self.linuxScript = os.path.dirname(os.path.realpath(__file__))+'/window-title'
        self.getForegroundWindowTitle = getattr(self, 'getForegroundWindowTitle'+platform.system())
        self.openDataFile()

    def openDataFile(self):
        self.closeDataFile()
        filename = checkDataDir() + time.strftime("/%d.txt", time.localtime())
        self.file = codecs.open(filename, "a", "utf-8")
        self.lastlocaltime = time.localtime()
        startline = 'start\t'+hhmmss(self.lastlocaltime)+'\t'+' '.join(platform.uname())+' '+''.join(platform.dist())+'\n'
        self.file.write(startline)
        self.lasttitle = ''
        self.startday = time.localtime().tm_mday
        self.lasttime = time.time()

    def getForegroundWindowTitleWindows(self):
        w = win32gui.GetForegroundWindow()
        title = win32gui.GetClassName(w)+' '+win32gui.GetWindowText(w)
        return unicode(title, 'gbk')

    def getForegroundWindowTitleLinux(self):
        p = subprocess.Popen(['sh', self.linuxScript], stdout=subprocess.PIPE)
        s = p.communicate()[0]
        title = s.replace('\n', ' ')
        return title

    def collect(self):
        day = time.localtime().tm_mday
        lasttime = self.lasttime
        self.lasttime = time.time()
        if (not self.startday == day) or (self.lasttime - lasttime > 60):
            self.openDataFile()

        title = self.getForegroundWindowTitle()
        if not title == self.lasttitle:
            self.lastlocaltime = time.localtime()
            data = hhmmss(self.lastlocaltime)+'\t'+title+'\n'
            self.file.write(data)
            self.flushData()
            self.lasttitle = title
            return data
        return ''

    def flushData(self):
            self.file.flush()

    def closeDataFile(self):
            if not None == self.file and not self.file.closed:
                    stopline = 'stop\t'+hhmmss(self.lastlocaltime)+'\n'
                    self.file.write(stopline)
                    self.flushData()
                    self.file.close()

    def main(self):
        atexit.register(self.closeDataFile)
        step = 2
        while True:
            time.sleep(step)
            self.collect()

    def start(self):
        thread = threading.Thread(target=self.main)
        thread.daemon = True
        thread.start()
        return thread

if __name__ == "__main__":
    tc = TimeCollector()
    tc.main()
