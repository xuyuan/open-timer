# -*- coding: utf-8 -*-
# update daily app usage

import re
import time
import webbrowser
import sys

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

    patternlist = createPatternList(patterndict)
    othercount = 0
    
    f = open(filename,'r')
    line = f.readline()
    laststs = None
    lastmatched = pstart
    while len(line) > 0:
        pmatched = pstart
        #print line,
        st = laststs
        if pstart.match(line):
            st = time.strptime(line[6:14],"%H:%M:%S")
            pmatched = pstart
        elif pstop.match(line):
            st = time.strptime(line[5:13],"%H:%M:%S")
            pmatched = pstop
        else:
            title = line[9:]
            matched = False
            st = time.strptime(line[:8],"%H:%M:%S")
            for p in patternlist:
                if p.match(title):
                    pmatched = p
                    matched = True
                    break
            if not matched:
                #print title,
                othercount = othercount + 1

        sts = st.tm_hour*3600+st.tm_min*60+st.tm_sec
        if not None == laststs:
            dt = sts - laststs
            lastmatched.addTime(dt)
        laststs = sts
        lastmatched = pmatched
            
        line = f.readline()

    tp = patternlist
    patternlist = []
    for p in tp:
        if p.count > 0 :
            patternlist.append(p)
    patternlist.sort()
    
    
    print
    print
    for p in patternlist:
        print p.name, p.count, p.time/60.0
    print 'other', othercount
    googlechartbhs(patternlist,filename)

def googlechartp3(pl):
    charturl = "http://chart.apis.google.com/chart?chs=600x200&cht=p3&chco=0000ff&chd=t:"
    for p in pl:
        charturl = charturl + str(p.time/3600.0) + ','
    charturl = charturl[:-1]
    charturl += '&chl='
    for p in pl:
        charturl = charturl + str(p.name) + '|'
    charturl = charturl[:-1]
    webbrowser.open(charturl)

def googlechartbhs(pl,title):
    # type
    charturl = "http://chart.apis.google.com/chart?cht=bhs&chco=0000ff"
    # size
    charturl += "&chs=600x"+ str(len(pl)*30+10)
    # data
    charturl += "&chd=t:"
    for p in pl:
        charturl = charturl + str(p.time/720.0) + ','
    charturl = charturl[:-1]
    # title
    charturl += "&chtt=Your time in "+title[5:-4]
    # label
    charturl += '&chxt=y&chxl=0:|'
    labelstr = ''
    for p in pl:
        labelstr = str(p.name) + '|' + labelstr
    labelstr = labelstr[:-1]
    charturl += labelstr
    # mark
    chmstr = '&chm='
    i = 0
    for p in pl:
        chmstr += 't'+p.timeStr()+',000000,0,'+str(i)+',13|'
        i+=1
    chmstr = chmstr[:-1]
    charturl += chmstr
    
    webbrowser.open(charturl)

def main(argv):
    if len(argv) == 0:
        todayfile = time.strftime('data/%Y/%m/%d.txt', time.localtime())
        update(todayfile)
    else:
        update(argv[0])

if __name__=="__main__":
    main(sys.argv[1:])
