#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The system tray of pytimer: a simple GUI.

Dependence:
   wxPython(www.wxpython.org)
"""
__author__ = 'Xu, Yuan'

import sys
import wx
from timecollector import TimeCollector
import updatedailyappusage

class TimeSaverTaskBarIcon(wx.TaskBarIcon):
    def __init__(self, parent):
        wx.TaskBarIcon.__init__(self)
        self.parentApp = parent
        self.CreateMenu()
    
    def CreateMenu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.ShowMenu)

        self.menu = wx.Menu()
        self.menu.Append(101, '&Resume')
        self.menu.Append(102, '&Today')
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, '&Close')

    def ShowMenu(self, event):
        self.PopupMenu(self.menu)

class TimeSaver(wx.Frame):
    def __init__(self):
        title = 'TimeSaver'
        size = (500, 500)
        wx.Frame.__init__(self, parent=None, title=title, size=size)

        self.icon = wx.Icon('logo.png',wx.BITMAP_TYPE_PNG)
        self.SetIcon(self.icon)
        
        # then initial a panel
        panel = wx.Panel(parent=self)
        self.panel = panel

        # a multi-line text
        self.text = wx.TextCtrl(panel,style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.HSCROLL)
        
        # resize event
        self.Bind(wx.EVT_SIZE, self.OnSize)
        # minimize event
        self.Bind(wx.EVT_ICONIZE, self.OnMinimize)
        # close event
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # toolbar
        #self.tb = self.CreateToolBar()

        # status bar
        self.CreateStatusBar()

        # Task Bar Icon
        self.tray = TimeSaverTaskBarIcon(self)
        self.tray.Bind(wx.EVT_MENU, self.OnMenuClose, id=wx.ID_EXIT)
        self.tray.Bind(wx.EVT_MENU, self.OnResume, id=101)
        self.tray.Bind(wx.EVT_MENU, self.onToday, id=102)
        self.tray.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnResume)
        self.tray.SetIcon(self.icon)

        #####
        self.timecollector = TimeCollector()
        self.timer = wx.Timer(panel)
        wx.EVT_TIMER(panel, self.timer.GetId(), self.onTimer)

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

    def OnSize(self, event):    
        size = self.GetClientSize()
        self.text.SetSize(size)
        self.panel.SetSize(size)
        event.Skip()

    def log(self, string):
        self.text.AppendText(string)

    def start(self):
            self.timer.Start(2000)

    def onTimer(self,event):
        data = self.timecollector.collect()
        if self.IsShown():
            self.log(data)

    def onToday(self,event):
        updatedailyappusage.main([])
        event.Skip()

def main():
    app = wx.App(False)
    frame = TimeSaver()
    frame.start()
    app.MainLoop()

if __name__ == '__main__':
    main()
