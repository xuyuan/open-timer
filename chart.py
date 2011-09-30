
from OpenFlashChart import Chart


class Pie():
    def __init__(self, data):
        pie = Chart()
        pie.type = "pie"
        pie.tip = "#percent#<br>#val# of #total#"
        pie.colours = ["ff3333", "#33ff66", "#0066cc"]
        pie.values = []
        for v in data:
            pie.values.append({"value": v.time(), "label": v.name})
        self.chart = Chart()
        self.chart.bg_colour = '#FFFFFF'
        self.chart.elements = [pie]

    def json(self):
        return self.chart.create()


class Bar():
    def __init__(self, data):
        bar = Chart()
        bar.type = "bar_sketch"
        bar.values = []
        values = []
        for v in data:
            values.append(v.time())
            bar.values.append({"top": v.time(), "tip": v.name + "<br>#val#"})
            bar.on_show.type = "grow-up"

        self.chart = Chart()
        if len(values) is not 0:
            self.chart.y_axis.max = max(values) * 1.1
        self.chart.x_axis.labels.rotate = -45
        self.chart.x_axis.labels.labels = []
        for v in data:
            self.chart.x_axis.labels.labels.append(v.name)
        self.chart.bg_colour = '#FFFFFF'

        self.chart.elements = [bar]

    def json(self):
        return self.chart.create()