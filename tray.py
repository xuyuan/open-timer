#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The system tray of pytimer: a simple GUI.

Dependence:
   wxPython(www.wxpython.org)
"""
__author__ = 'Xu, Yuan'

import sys
import os
import wx
from timecollector import TimeCollector
import webbrowser


class TimeSaverTaskBarIcon(wx.TaskBarIcon):
    """indicator"""
    def __init__(self, parent):
        wx.TaskBarIcon.__init__(self)
        self.parentApp = parent
        self.CreateMenu()

    def CreateMenu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.ShowMenu)

        self.menu = wx.Menu()
        self.menu.Append(101, '&Resume')
        self.menu.Append(102, '&Dashboard')
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, '&Close')

    def ShowMenu(self, event):
        self.PopupMenu(self.menu)


class LogViewer(wx.Panel):
    """panel displays logs"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # a multi-line text
        self.text = wx.TextCtrl(self,
                        style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.HSCROLL)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.text, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()

    def log(self, string):
        self.text.AppendText(string)


class TimeSaver(wx.Frame):
    """main frame"""
    def __init__(self):
        title = 'TimeSaver'
        size = (500, 500)
        wx.Frame.__init__(self, parent=None, title=title, size=size)

        self.icon = wx.Icon(os.path.join(os.path.dirname(__file__),
                                'logo.png'),
                            wx.BITMAP_TYPE_PNG)
        self.SetIcon(self.icon)

        # tabs
        self.logViewer = LogViewer(self)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.logViewer, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()

        # minimize event
        self.Bind(wx.EVT_ICONIZE, self.OnMinimize)
        # close event
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # toolbar
        #self.tb = self.CreateToolBar()

        # status bar
        #self.CreateStatusBar()

        # Task Bar Icon
        self.tray = TimeSaverTaskBarIcon(self)
        self.tray.Bind(wx.EVT_MENU, self.OnMenuClose, id=wx.ID_EXIT)
        self.tray.Bind(wx.EVT_MENU, self.OnResume, id=101)
        self.tray.Bind(wx.EVT_MENU, self.onDashboard, id=102)
        self.tray.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnResume)
        self.tray.SetIcon(self.icon)

        #####
        self.timecollector = TimeCollector()
        self.timer = wx.Timer(self)
        wx.EVT_TIMER(self, self.timer.GetId(), self.onTimer)

    def OnResume(self, event):
            self.Show(not self.IsShown())
            if self.IsShown():
                self.SetFocus()

    def OnMenuClose(self, event):
        self.OnClose(event)
        sys.exit()

    def OnClose(self, event):
        self.timer.Stop()
        self.timecollector.closeDataFile()
        # destroy task bar icon before close this frame
        self.tray.RemoveIcon()
        self.tray.Destroy()
        event.Skip()

    def OnMinimize(self, event):
        self.Show(False)
        event.Skip()

    def start(self):
            self.timer.Start(2000)

    def onTimer(self, event):
        data = self.timecollector.collect()
        if self.IsShown():
            self.logViewer.log(data)

    def onDashboard(self, event):
        webbrowser.open('http://localhost::8080/dashboard/index.html')
        event.Skip()


def main():
    app = wx.App(False)
    frame = TimeSaver()
    frame.start()
    app.MainLoop()

if __name__ == '__main__':
    main()