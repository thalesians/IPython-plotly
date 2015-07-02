__author__ = 'saeedamen'

"""
    Thalesians Ltd (www.pythalesians.com) please contact saeed@pythalesians.com for further information
    You are free to modify and distribute this code as you see fit provided this source is cited
"""
# for time series/maths
import math
from datetime import timedelta
import time

# Flask application
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

# for plotting
import json
import plotly

# Dash components
import dash.utils as utils
from dash.components import element as el
from dash.components import graph

# for time series manipulation
import pandas
import pandas.io.data as web

import datetime

from datadownloader import DataDownloader

def load_data():
    ticker = 'EURUSD' # will use in plot titles later (and for creating Plotly URL)

    ##### download intraday EUR/USD data from Bloomberg or CSV file
    source = "Bloomberg"
    source = "CSV"

    csv_file = None

    data_downloader = DataDownloader()
    start_date = datetime.datetime.utcnow() - timedelta(days = 120)
    freq = 'intraday'

    if source == 'Bloomberg':
        vendor_ticker = 'EURUSD BGN Curncy'
    elif source == 'CSV':
        # you can get free FX intraday data from Gain Capital (if you don't have Bloomberg)
        vendor_ticker = 'EURUSD'
        csv_file = 'D:/EURUSD.csv'

    return data_downloader.download_time_series(vendor_ticker, ticker, start_date, source, csv_file = csv_file, freq = freq)

# define properties for application
name = 'dash-realised-vol-slide'
app = Flask(name)
app.debug = True
app.config['key'] = 'secret'
app.config['last'] = time.time()
socketio = SocketIO(app)
spot = load_data()
graph_id = 'realised-vol-slider'

# write the HTML "includes" blocks to /templates/runtime/dash-1-hello-world
# alternatively, include the HTML yourself in that folder
utils.write_templates(
    {
        'header': [
            el('H1', {}, 'Dash to investigate realised vol')
        ],

        'controls': [
            el('label', {}, 'Frequency 5 to 60 mins'),
            el('input', {
                'type': 'range',
                'class': 'u-full-width show-values',
                'name': 'frequency',
                'value': 0,
                'min': 5,
                'max': 60,
                'step': 5
            }),
            el('label', {}, 'Period 1 to 20 days'),
            el('input', {
                    'type': 'range',
                    'class': 'u-full-width show-values',
                    'name': 'period',
                    'value': 0,
                    'min': 1,
                    'max': 20,
                    'step': 1
                }),
            el('label', {}, 'Title'),
            el('input', {
                'type': 'text',
                'name': 'title',
                'placeholder': 'Type away',
                'class': 'u-full-width'
            }, '')
        ],

        'main_pane': [
            graph(graph_id)
        ]
    }, name
)

@app.route('/')
def index():
    return render_template('layouts/layout_single_column_and_controls.html',
                           app_name = name)

@socketio.on('replot')
def replot(app_state):
    print(app_state) # for debugging

    frequency = float(app_state['frequency'])
    period = float(app_state['period'])
    period_mins = period * (1440.0 / frequency)

    # resample data for minute frequency specified
    resampled = spot.loc[spot.index.minute % frequency == 0]
    resampled = resampled.dropna()

    # calculate returns (need for realised volatility calculation)
    rets = resampled / resampled.shift(1) - 1

    # calculate realised volatility (careful with annualisation factor!)
    vol = pandas.rolling_std(rets, period_mins) * math.sqrt(252.0 * (1440.0 / frequency)) * 100

    # resample to daily data (quicker to plot)
    to_plot = vol.loc[vol.index.hour % 20 == 0]
    to_plot = to_plot.loc[to_plot.index.minute % 60 == 0]

    x = pandas.to_datetime(to_plot.index.values, format='%Y-%m-%d %H:%M')
    y = to_plot.ix[:,0]

    # define graph in JSON format
    messages = [
        {
            'id': graph_id,
            'task': 'newPlot',
            'data': [{
                'x': x,
                'y': y
            }],
            'layout': {
                'xaxis': {
                    'title' : 'Date'
                },
                'yaxis': {
                    'title' : 'Vol'
                },
                'title': app_state.get('title', '') + 'freq = ' + str(frequency) + ' mins, period = '
                         + str(period) + ' days, ' + str(period_mins) + ' points'
            }
        }
    ]

    # post JSON message
    emit('postMessage', json.dumps(messages, cls = plotly.utils.PlotlyJSONEncoder))

if __name__ == '__main__':
    socketio.run(app)
