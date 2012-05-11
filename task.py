"""
A simple task rememinder: After starting (checking in) a task, the program
will rememinder you when you use a program which is not in the list of task.
"""

__author__ = 'Xu, Yuan'

import os
import pickle
import re
import json
import wx
from wx.lib.intctrl import IntCtrl

from dict import appdict


class Task(object):
    def __init__(self, apps, maxDistraction):
        self.setApps(apps)

        self.maxDistraction = maxDistraction

        self.distracting = False
        self.distraction = 0

    def setApps(self, apps):
        self.appNames = apps
        self.apps = []
        for name in self.appNames.split(' '):
            if name in appdict:
                self.apps.append(re.compile(appdict[name]))
            else:
                wx.MessageBox('unknown app: ' + name)

    def start(self):
        print 'start task v2'

    def stop(self):
        self.distracting = False
        self.distraction = 0

    def update(self, data, step):
        if data:
            line = data[9:]
            self.distracting = False
            for app in self.apps:
                if not app.match(line):
                    self.distracting = True
        if self.distracting:
            self.distraction += step
        else:
            self.distraction = 0

        if self.maxDistraction > 0 and self.distraction > self.maxDistraction:
            wx.MessageBox('what are u doing?!!', 'You are wasting time!')

    def loads(self, jsonStr):
        '''load from json'''
        pass

    def dumps(self):
        '''dumps to json'''
        print json.dumps({'apps': self.appNames,
                    'maxDistraction': self.maxDistraction})
        pass


class TaskManager(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box)

        self.dataDir = os.path.join(os.path.dirname(__file__), 'data/task')
        self.tasks = {}

        self.taskChoser = wx.ComboBox(self, style=wx.CB_READONLY)
        self.taskChoser.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        box.Add(self.taskChoser)

        grid = wx.GridSizer(4, 2)
        box.Add(grid)

        self.taskName = wx.TextCtrl(self)

        self.appsInput = wx.TextCtrl(self)

        self.maxDistractionInput = IntCtrl(self, value=0, min=0)

        deleteButton = wx.Button(self, label='Delete')
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDelete)
        cancelButton = wx.Button(self, label='Cancel')
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        saveButton = wx.Button(self, label='Save')
        saveButton.Bind(wx.EVT_BUTTON, self.OnSave)

        grid.AddMany([
            (wx.StaticText(self, label='Name:'), 0, wx.EXPAND),
            (self.taskName, 0, wx.EXPAND),

            (wx.StaticText(self, label='Apps:'), 0, wx.EXPAND),
            (self.appsInput, 0, wx.EXPAND),

            (wx.StaticText(self, label='Max. Distraction:'), 0, wx.EXPAND),
            (self.maxDistractionInput, 0, wx.EXPAND),

                     (deleteButton), (cancelButton), (saveButton)])

        self.refresh()

    def OnDelete(self, event):
        if self.taskName.GetValue():
            dlg = wx.MessageDialog(self,
                    "Do you really want to delete this task?",
                    "Delete " + self.taskName.GetValue(),
                    wx.OK | wx.CANCEL)
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                filePath = os.path.join(self.dataDir, self.taskName.GetValue())
                os.remove(filePath)
                del self.tasks[self.taskName.GetValue()]
                self.refresh()

    def OnSave(self, event):
        if self.taskName.GetValue():
            filePath = os.path.join(self.dataDir, self.taskName.GetValue())
            t = Task(self.appsInput.GetValue(),
                     self.maxDistractionInput.GetValue())
            pickle.dump(t, open(filePath, 'w'))
            self.refresh(self.taskName.GetValue())

    def OnCancel(self, event):
        self.refresh(self.taskChoser.GetValue())

    def refresh(self, selectedTask=None):
        taskList = os.listdir(self.dataDir)
        self.taskChoser.Clear()
        for name in taskList:
            self.taskChoser.Append(name)
            if name:
                filePath = os.path.join(self.dataDir, name)
                t = pickle.load(open(filePath))
                self.tasks[name] = t
        if selectedTask:
            self.taskChoser.SetStringSelection(selectedTask)
        else:
            self.taskChoser.SetSelection(0)
        self.OnSelect(None)

    def OnSelect(self, event):
        name = self.taskChoser.GetValue()
        if name:
            self.taskName.SetValue(name)
            t = self.tasks[name]
            self.appsInput.SetValue(t.appNames)
            self.maxDistractionInput.SetValue(t.maxDistraction)