# -*- coding: utf-8 -*-
"""
 Abstract class
"""
__author__ = 'Xu, Yuan'

class Widget:
    def __init__(self, name, dataTable):
        self.name = name
        self.dataTable = dataTable

    def head(self):
        return ''

    def body(self):
        return "<H1>"+(self.name)+"</H1>"+'<div id ="'+(self.name)+'"></div>\n'
