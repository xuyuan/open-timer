#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 update daily usage
"""
__author__ = 'Xu, Yuan'

import re
import time
import webbrowser
import sys
import googlechart

class Application():
    def __init__(self, n, s):
        self.name = n
        self.p = re.compile(s)
        self.count = 0
        self.t = 0

    def match(self,s):
        if self.p.match(s):
            self.count += 1
            return True
        else:
            return False

    def addTime(self,t):
        self.t += t

    def __cmp__(self, other):
        return other.time() - self.time()

    def time(self):
        return self.t

def createListFromDict(type,sd):
    pl = []
    for x in sd.keys():
        pl.append(type(x,sd[x]))
    return pl

def removeZeroTime(l):
    r = []
    for e in l:
        if e.time() > 0 :
            r.append(e)
    return r
    
class Category():
    """
    Application category according to its function
    """
    def __init__(self,n,s):
        self.name = n
        self.p = re.compile(s)
        self.apps = []

    def match(self,app):
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

def updateApp(filename):
    appdict = {
        # windows applications
        'WindowsFileSystem':'^CabinetWClass',
        'Chrome':'^Chrome_',
        'IE':'^IEFrame.*Windows Internet Explorer\r$',
        'Notepad':'^Notepad',
        'WindowsPhotoViewer':'^Photo_Lightweight_Viewer',
        'TTPlayer':'^TTPlayer_',
        'WindowsConsole':'^ConsoleWindowClass',
        'TortoiseSVN':'.*TortoiseSVN\r$',
        'GIMP':'.*GIMP\r$|^gdkWindowToplevel',
        'AdobeReader':'.*Adobe Reader\r$',
        'FunshionPlayer':'^funshion_player_tzdenjohn',
        'WindowsProgramManager':'^Progman Program Manager',
        'WindowsMediaPlayer':'^WMPlayerApp Windows Media Player',
        'OpenOffice':'.*OpenOffice.org Calc$',
        'DigitalPhotoProfessional':'^ATL:0043D110 Digital Photo Professional|^#32770 Digital Photo Professional',
        'StormPlayer':'^Afx:400000:3:10003:2:',
        'MSN':'^IMWindowClass|.*Windows Live Messenger$',
        # Linux applications
        'Firefox':'^ "Navigator", "Firefox"|^ "Dialog", "Firefox"',
        'GnomeTerminal':'^ "gnome-terminal"',
        'Kpdf':'^ "kpdf"',
        'Desktop':'^ "desktop_window"',
        'Nautilus':'^ "nautilus"|^ "file_properties", "Nautilus"',
        'Gedit':'^ "gedit"',
        'GnomeSetting':'^ "gnome-control-center"|^ "gnome-appearance-properties"',
        'Yast':'^ "y2controlcenter-gnome"|^ "y2base"',
        # Linux & Windows
        'Emacs':'^Emacs|^ "emacs"',
        'QQ':'^TXGuiFoundation|^ "qq"',
        'OpenOffice':'^ "VCLSalFrame", "OpenOffice.org 3.0"',
        'Skype':'^ "skype"',
        'Pidgin':'^ "pidgin"',
        'Python':'^TkTopLevel|^Shell_TrayWnd|^ "python"'
        }

    pstart = Application('start','^start')
    pstop = Application('stop','^stop')
    other = Application('other','.')

    applist = createListFromDict(Application,appdict)
    
    
    f = open(filename,'r')
    line = f.readline()
    laststs = None
    lastmatched = pstart
    while len(line) > 0:
        pmatched = None
        #print line,
        st = laststs
        if pstart.match(line):
            st = time.strptime(line[6:14],"%H:%M:%S")
            pmatched = pstart
            laststs = st.tm_hour*3600+st.tm_min*60+st.tm_sec
        elif pstop.match(line):
            st = time.strptime(line[5:13],"%H:%M:%S")
            pmatched = pstop
            sts = st.tm_hour*3600+st.tm_min*60+st.tm_sec
            dt = sts - laststs
            lastmatched.addTime(dt)
            laststs = sts
        else:
            ismatched = False
            title = line[9:]
            st = time.strptime(line[:8],"%H:%M:%S")
            sts = st.tm_hour*3600+st.tm_min*60+st.tm_sec
            dt = sts - laststs
            lastmatched.addTime(dt)
            for a in applist:
                if a.match(title):
                    pmatched = a
                    ismatched = True
                    break
            if not ismatched:
                #print title,
                other.match(title)
                pmatched = other
                
            laststs = sts
            lastmatched = pmatched
        
            
        line = f.readline()

    applist = removeZeroTime(applist)
    applist.sort()
    if other.time() > 0 :
        applist.append(other)
    
    #print
    #print
    #for p in patternlist:
    #    print p.name, p.count, p.time/60.0

    return applist

def updateCategory(applist):
    categoryDict = {
        'InternetBrowser':'Firefox|Chrome|IE',
        'Editor':'Emacs|Notepad|Gedit',
        'PdfReader':'Kpdf|AdobeReader',
        'Console':'WindowsConsole|GnomeTerminal',
        'Messanger':'QQ|Pidgin|Skype|MSN',
        'Video/Music':'StormPlayer|TTPlayer',
        'SystemUtilities':'WindowsFileSystem|Nautilus|GnomeSetting|Yast',
        'Office':'OpenOffice'
        }

    categoryList = createListFromDict(Category,categoryDict)
    other = Category('Uncategorized','.')
    for app in applist:
        ismatched = False
        for c in categoryList:
            if c.match(app):
                ismatched = True
                break
        if not ismatched:
            other.match(app)
    
    categoryList = removeZeroTime(categoryList)
    categoryList.sort()
    if other.time() > 0 :
        categoryList.append(other)

    return categoryList

def main(argv):
    file = None
    if len(argv) == 0:
        file = time.strftime('data/%Y/%m/%d.txt', time.localtime())
    else:
        file = argv[0]

    pl = updateApp(file)
    cl = updateCategory(pl)
        
    # draw figure
    charturl = googlechart.bhs(pl,'Your time @ '+file+' (Application)')
    webbrowser.open(charturl)
    charturl = googlechart.bhs(cl,'Your time @ '+file+' (Category)')
    webbrowser.open(charturl)

if __name__=="__main__":
    main(sys.argv[1:])
