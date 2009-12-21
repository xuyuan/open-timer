# -*- coding: utf-8 -*-
"""
 Generate Table
"""
__author__ = 'Xu, Yuan'

from Widget import Widget

class Table(Widget):
    def __init__(self, name, dataTable, format='showRowNumber: true'):
        Widget.__init__(self, name, dataTable)
        self.__format = format
        self.__template = """
    <script>
      google.load("visualization", "1", {packages:["table"]});

      google.setOnLoadCallback(drawTable);
      function drawTable() {
        var table = new google.visualization.Table(document.getElementById('%(name)s'));
        var data = new google.visualization.DataTable(%(json)s, 0.5);
        table.draw(data, {%(format)s});
      }
    </script>
"""

    def head(self):
        # Creating a JSon string
        json = self.dataTable.ToJSon()#order_by=None
        name = self.name
        format = self.__format
        return self.__template % vars()
