# -*- coding: utf-8 -*-
"""
 Generate html file
"""
__author__ = 'Xu, Yuan'

class Html:
    def __init__(self,title):
        self.__title = title
        self.__elements = []
        self.__template = """
<html>
  <head>
    <title>%(title)s</title>
    <script src="http://www.google.com/jsapi" type="text/javascript"></script>
    %(headContent)s
  </head>
  <body>
    %(bodyContent)s
  </body>
</html>
"""

    def add(self,e):
        self.__elements.append(e)

    def head(self):
        headString = ''
        for e in self.__elements:
            headString += e.head()
        return headString
    
    def body(self):
        bodyString = ''
        for e in self.__elements:
            bodyString += e.body()
        return bodyString

    def all(self):
        bodyContent = self.body()
        headContent = self.head()
        title = self.__title
        return self.__template % vars()

    def write(self, filename):
        htmlfile = open(filename, 'w')
        htmlfile.write(self.all())
        htmlfile.close()
