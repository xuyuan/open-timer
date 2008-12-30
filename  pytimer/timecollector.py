#!/usr/bin/env python

import sys
import time
import os
import platform

if platform.system() == 'Windows':
	import win32gui
elif platform.system() == 'Linux':
	import subprocess

def makeSureDir(dir):
        if not os.path.isdir(dir):
                os.mkdir(dir)

def checkDataDir():
        datadir = "data"
        makeSureDir(datadir)
        datadir += time.strftime("/%Y",time.localtime())
        makeSureDir(datadir)
        datadir += time.strftime("/%m",time.localtime())
        makeSureDir(datadir)
        return datadir

def hhmmss():
        return time.strftime("%H:%M:%S",time.localtime())

class TimeCollector():
        def __init__(self):
                self.file = None
		self.getForegroundWindowTitle = getattr(self, 'getForegroundWindowTitle'+platform.system())
                self.openDataFile()

        def openDataFile(self):
                self.closeDataFile()
                filename = checkDataDir() + time.strftime("/%d.txt",time.localtime())
                self.file = open(filename,'a')
                startline = 'start\t'+hhmmss()+'\t'+' '.join(platform.uname())+' '+''.join(platform.dist())+'\n'
                self.file.write(startline)
                self.lasttitle = ''
                self.startday = time.localtime().tm_mday

	def getForegroundWindowTitleWindows(self):
		w = win32gui.GetForegroundWindow()
                return win32gui.GetClassName(w)+' '+win32gui.GetWindowText(w)

	def getForegroundWindowTitleLinux(self):
		s = subprocess.Popen('./window-title', stdout=subprocess.PIPE).communicate()[0]
		return s.replace('\n',' ');
                
        def collect(self):
                day = time.localtime().tm_mday
                if not self.startday == day:
                        self.openDataFile()
                        
                title = self.getForegroundWindowTitle()
                if not title == self.lasttitle:
                        data = hhmmss()+'\t'+title+'\n'
                        self.file.write(data)
                        self.lasttitle = title
                        return data
                return ''

        def flushData(self):
                self.file.flush()

        def closeDataFile(self):
                if not None == self.file and not self.file.closed:
                        stopline = 'stop\t'+hhmmss()+'\n'
                        self.file.write(stopline)
                        self.flushData()
                        self.file.close()
                                
        def main(self):
                step = 2
                while True:
                        time.sleep(step)
                        self.collect()
                        


if __name__=="__main__":
        tc = TimeCollector()
        tc.main()
