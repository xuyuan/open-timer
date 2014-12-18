#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
simple web server for dashboard
"""
__author__ = 'Xu, Yuan'

from flask import Flask, render_template, request
from day import Day
from week import Week
from month import Month
from year import Year
from chart import Pie, Bar

app = Flask(__name__)
the_data = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/set_time')
def set_time():
    period = request.args.get('period')
    yy = int(request.args.get('yy'))
    mm = int(request.args.get('mm'))
    dd = int(request.args.get('dd'))
    global the_data
    if period == 'year':
        the_data = Year(yy)
    elif period == 'month':
        the_data = Month(yy, mm)
    elif period == 'week':
        the_data = Week(yy, mm, dd)
    else:
        the_data = Day(yy, mm, dd)
    return the_data.info


def get_data():
    global the_data
    if the_data is None:
        the_data = Day()
    return the_data


def create_chart(data, chart):
    if chart == 'pie':
        return Pie(data).json()
    elif chart == 'bar':
        return Bar(data).json()


@app.route('/category_list/<chart>')
def category_list(chart):
    return create_chart(get_data().categoryList, chart)


@app.route('/application_list/<chart>')
def application_list(chart):
    return create_chart(get_data().applicationList, chart)


if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://localhost:5050')
    app.run(port=5050, debug=True)
