# -*- coding: utf-8 -*-
"""
 Generate Pie Chart
"""
__author__ = 'Xu, Yuan'

from Widget import Widget

class PieChart(Widget):
    def __init__(self, name, dataTable):
        Widget.__init__(self, name, dataTable)
        self.__template = """
<script>
      google.load("visualization", "1", {packages:["piechart"]});

      google.setOnLoadCallback(drawPieChart);
      function drawPieChart() {
        var chart = new google.visualization.PieChart(document.getElementById('%(name)s'));
        var data = new google.visualization.DataTable(%(json)s, 0.5);
        chart.draw(data, {width: 400, height: 240, is3D: true, title: '%(name)s'});
      }
</script>
"""

    def head(self):
        # Creating a JSon string
        json = self.dataTable.ToJSon()
        name = self.name
        return self.__template  % vars()
