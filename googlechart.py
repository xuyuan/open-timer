# -*- coding: utf-8 -*-
"""
 Generate charts using Google Chart,
 please visit http://code.google.com/intl/en/apis/chart/
 for more information
"""
__author__ = 'Xu, Yuan'

def bhs(pl,title):
    """
    Horizontal bar chart, with stacked bars.
    """
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
        chmstr += 't'+p.timeStr()+',000000,0,'+str(i)+',13|'
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
