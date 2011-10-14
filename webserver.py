#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
simple web server for dashboard
"""
__author__ = 'Xu, Yuan'

import cgi
from os import path
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from day import Day
from week import Week
from month import Month
from year import Year
from chart import Pie, Bar

theData = None
dirname = path.dirname(__file__)

class PytimerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            filename = self.path
            if (filename.endswith(".html") or filename.endswith(".css")
                or filename.endswith(".js") or filename.endswith(".swf")
                or filename.endswith(".png")):
                f = open(path.join(dirname, filename[1:]))
                self.send_response(200)
                self.send_header('Content-type', 'text/'
                                + filename[filename.rfind('.') + 1:])
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            else:  # our dynamic content
                self.executeCommand()
                return

            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(
                                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query = cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)

            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            self.wfile.write("<HTML>POST OK.<BR><BR>")
            self.wfile.write(upfilecontent[0])

        except:
            pass

    def do_OPTIONS(self):
        self.executeCommand()

    def executeCommand(self):
        global theData
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        cmd = self.path[1:]
        print cmd
        if cmd.find('=') == -1:
            s = eval(cmd)
            self.wfile.write(s)
        else:
            exec cmd
            self.wfile.write("exec " + cmd)

    def setDay(self, yy, mm, dd):
        global theData
        theData = Day(yy, mm, dd)
        return theData.info

    def setWeek(self, yy, mm, dd):
        global theData
        theData = Week(yy, mm, dd)
        return theData.info

    def setMonth(self, yy, mm, dd):
        global theData
        theData = Month(yy, mm)
        return theData.info

    def setYear(self, yy, mm, dd):
        global theData
        theData = Year(yy)
        return theData.info

    def getData(self):
        global theData
        if theData is None:
            theData = Day()
        return theData


def main():
    try:
        server = HTTPServer(('', 8080), PytimerHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()