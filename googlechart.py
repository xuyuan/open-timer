# -*- coding: utf-8 -*-
"""
 Generate charts using Google Chart,
 please visit http://code.google.com/intl/en/apis/chart/
 for more information
"""
__author__ = 'Xu, Yuan'

def second2Str(sec):
    h = sec / 3600
    t = sec % 3600
    m = t / 60
    s = t % 60
    ts = str(m) + 'm' + str(s) +'s'
    if h > 0:
        ts = str(h) + 'h' + ts
    return ts

def bhs(pl,title):
    """
    Horizontal bar chart, with stacked bars.
    """
    pl = pl[:15] # Chart may contain at most 300000, pixels.
    # type
    charturl = "http://chart.apis.google.com/chart?cht=bhs&chco=0000ff"
    # size
    charturl += "&chs=600x"+ str(len(pl)*30+10)
    # data
    charturl += "&chd=t:"
    for p in pl:
        charturl = charturl + str(p.time()/720.0) + ','
    charturl = charturl[:-1]
    # title
    charturl += "&chtt="+title
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
        chmstr += 't'+second2Str(p.time())+',000000,0,'+str(i)+',13|'
        i+=1
    chmstr = chmstr[:-1]
    charturl += chmstr

    return charturl

def p3(pl):
    """
    Three dimensional pie chart.
    """
    charturl = "http://chart.apis.google.com/chart?chs=600x200&cht=p3&chco=0000ff&chd=t:"
    for p in pl:
        charturl = charturl + str(p.time/3600.0) + ','
    charturl = charturl[:-1]
    charturl += '&chl='
    for p in pl:
        charturl = charturl + str(p.name) + '|'
    charturl = charturl[:-1]
    return charturl
