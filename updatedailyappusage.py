# -*- coding: utf-8 -*-
"""
 update daily app usage
"""
__author__ = 'Xu, Yuan'

import re
import time
import webbrowser
import sys
import googlechart

class Pattern():
    def __init__(self, n, s):
        self.name = n
        self.p = re.compile(s)
        self.count = 0
        self.time = 0

    def match(self,s):
        if self.p.match(s):
            self.count += 1
            return True
        else:
            return False

    def addTime(self,t):
        self.time += t

    def __cmp__(self, other):
        return other.time - self.time

    def timeStr(self):
        h = self.time / 3600
        t = self.time % 3600
        m = t / 60
        s = t % 60
        ts = str(m) + 'm' + str(s) +'s'
        if h > 0:
            ts = str(h) + 'h' + ts
        return ts

def createPatternList(sd):
    pl = []
    for x in sd.keys():
        pl.append(Pattern(x,sd[x]))
    return pl
    

def update(filename):
    patterndict = {'WindowsFileSystem':'^CabinetWClass',
                   'Chrome':'^Chrome_',
                   'IE':'^IEFrame.*Windows Internet Explorer\r$',
                   'Python':'^TkTopLevel|^Shell_TrayWnd',
                   'Notepad':'^Notepad',
                   'Emacs':'^Emacs',
                   'WindowsPhotoViewer':'^Photo_Lightweight_Viewer',
                   'QQ':'TXGuiFoundation',
                   'TTPlayer':'^TTPlayer_',
                   'WindowsConsole':'^ConsoleWindowClass',
                   'TortoiseSVN':'.*TortoiseSVN\r$',
                   'GIMP':'.*GIMP\r$|^gdkWindowToplevel',
                   'AdobeReader':'.*Adobe Reader\r$',
                   'FunshionPlayer':'^funshion_player_tzdenjohn',
                   'WindowsProgramManager':'^Progman Program Manager',
                   'WindowsMediaPlayer':'^WMPlayerApp Windows Media Player',
                   'OpenOffice':'.*OpenOffice.org Calc$',
                   'DigitalPhotoProfessional':'^ATL:0043D110 Digital Photo Professional|^#32770 Digital Photo Professional'}

    pstart = Pattern('start','^start')
    pstop = Pattern('stop','^stop')
    other = Pattern('other','.')

    patternlist = createPatternList(patterndict)
    
    
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
            for p in patternlist:
                if p.match(title):
                    pmatched = p
                    ismatched = True
                    break
            if not ismatched:
                #print title,
                other.match(title)
                pmatched = other
                
            laststs = sts
            lastmatched = pmatched
        
            
        line = f.readline()

    tp = patternlist
    patternlist = []
    for p in tp:
        if p.count > 0 :
            patternlist.append(p)
    patternlist.append(other)
    patternlist.sort()
    
    #print
    #print
    #for p in patternlist:
    #    print p.name, p.count, p.time/60.0

    return patternlist

def main(argv):
    file = None
    if len(argv) == 0:
        file = time.strftime('data/%Y/%m/%d.txt', time.localtime())
    else:
        file = argv[0]

    pl = update(file)
        
    # draw figure
    charturl = googlechart.bhs(pl,'Your time @ '+file)
    webbrowser.open(charturl)

if __name__=="__main__":
    main(sys.argv[1:])
