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
from task import TaskManager
import webbrowser


class TimeSaverTaskBarIcon(wx.TaskBarIcon):
    """indicator"""
    def __init__(self, parent):
        wx.TaskBarIcon.__init__(self)
        self.parent = parent
        self.CreateMenu()

    def CreateMenu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.ShowMenu)

        self.taskmenu = wx.Menu()

        self.menu = wx.Menu()
        self.menu.AppendMenu(101, '&Task', self.taskmenu)
        self.menu.Append(102, '&Resume')
        dashboardButton = self.menu.Append(-1, '&Dashboard')
        self.Bind(wx.EVT_MENU, self.onDashboard, dashboardButton)
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, '&Close')

    def ShowMenu(self, event):
        self.PopupMenu(self.menu)

    def UpdateTasks(self, tasks):
        id = wx.NewId()
        menuItem = self.taskmenu.Append(id, 'None', kind=wx.ITEM_RADIO)
        self.taskmenu.Bind(wx.EVT_MENU, self.CheckOut, menuItem)
        for t in tasks:
            id = wx.NewId()
            menuItem = self.taskmenu.Append(id, t, kind=wx.ITEM_RADIO)
            self.taskmenu.Bind(wx.EVT_MENU, self.CheckIn, menuItem)

    def CheckOut(self, event):
        self.parent.CheckOut()

    def CheckIn(self, event):
        id = event.GetId()
        item = self.taskmenu.FindItemById(id)
        self.parent.CheckIn(item.GetLabel())

    def onDashboard(self, event):
        webbrowser.open('http://localhost::8080/dashboard/index.html')
        event.Skip()


class LogViewer(wx.Panel):
    """panel displays logs"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # a multi-line text
        self.text = wx.TextCtrl(self,
                        style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.HSCROLL)

        box = wx.BoxSizer()
        box.Add(self.text, 1, wx.EXPAND)
        self.SetSizer(box)

    def log(self, string):
        self.text.AppendText(string)


class TimeSaver(wx.Frame):
    """main frame"""
    def __init__(self):
        title = 'Save My Time'
        size = (500, 500)
        self.step = 2000
        wx.Frame.__init__(self, parent=None, title=title, size=size)

        self.icon = wx.Icon(os.path.join(os.path.dirname(__file__),
                                'logo.png'),
                            wx.BITMAP_TYPE_PNG)
        self.SetIcon(self.icon)

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # tabs
        self.currentTask = None
        self.task = TaskManager(nb)
        nb.AddPage(self.task, "Task")

        self.logViewer = LogViewer(nb)
        nb.AddPage(self.logViewer, "Logging")

        box = wx.BoxSizer()
        box.Add(nb, 1, wx.EXPAND)
        p.SetSizer(box)

        # minimize event
        self.Bind(wx.EVT_ICONIZE, self.OnMinimize)
        # close event
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Task Bar Icon
        self.tray = TimeSaverTaskBarIcon(self)
        self.tray.Bind(wx.EVT_MENU, self.OnMenuClose, id=wx.ID_EXIT)
        self.tray.Bind(wx.EVT_MENU, self.OnResume, id=102)
        self.tray.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnResume)
        self.tray.SetIcon(self.icon)
        self.tray.UpdateTasks(self.task.tasks.keys())

        #####
        self.timecollector = TimeCollector()
        self.timer = wx.Timer(self)
        wx.EVT_TIMER(self, self.timer.GetId(), self.onTimer)

        self.Centre()

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
            self.timer.Start(self.step)

    def onTimer(self, event):
        data = self.timecollector.collect()
        if self.IsShown():
            self.logViewer.log(data)
        if self.currentTask:
            self.currentTask.update(data, self.step)

    def CheckOut(self):
        if self.currentTask:
            self.currentTask.stop()
            self.currentTask = None

    def CheckIn(self, task):
        newTask = self.task.tasks[task]
        if self.currentTask != newTask:
            self.CheckOut()
            self.currentTask = newTask
            self.currentTask.start()

def main():
    app = wx.App(False)
    frame = TimeSaver()
    frame.start()
    app.MainLoop()

if __name__ == '__main__':
    main()