__author__ = 'saeedamen'

"""
    Thalesians Ltd (www.pythalesians.com) please contact saeed@pythalesians.com for further information
    You are free to modify and distribute this code as you see fit provided this source is cited
"""

# for dates
import datetime
import time

# for plotting data
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

postfix = "test"

# for time series manipulation
import pandas
import pandas.io.data as web

import datetime

from datadownloader import DataDownloader

def streaming_fx_study():


    # Learn about API authentication here: https://plot.ly/python/getting-started
    # Find your api_key here: https://plot.ly/settings/api
    plotly_username = "thalesians"
    plotly_api_key = "XXXX"

    # Learn about stream id here at: http://help.plot.ly/documentation/python/streaming-tutorial/
    # Find your stream_id here: https://plot.ly/settings/api
    stream_id = "XXXX"

    plotly.tools.set_credentials_file(username=plotly_username, api_key=plotly_api_key)

    # Code below based on https://plot.ly/python/streaming-line-tutorial/
    max_points = 50000

    data_downloader = DataDownloader()

    ticker = 'EURUSD'; vendor_ticker = 'EURUSD=X'
    postfix = '-test'

    # Make instance of stream id object
    stream = plotly.graph_objs.Stream(
            token = stream_id,  # (!) link stream id to 'token' key
            maxpoints = max_points      # (!) keep a max of 80 pts on screen
    )

    trace1 = plotly.graph_objs.Scatter(
        x = [],
        y = [],
        mode = 'lines',
        stream = stream         # (!) embed stream id, 1 per trace
    )

    data = Data([trace1])

    # Add title to layout object
    layout = Layout(title = ticker)

    # Make a figure object
    fig = Figure(data = data, layout = layout)

    # Send fig to Plotly, initialize streaming plot, open new tab
    py.iplot(fig, filename=ticker + "-stream" + postfix)

    # Make instance of the Stream link object, with same stream id as Stream id object
    s = py.Stream(stream_id)

    # Open the stream
    s.open()

    #### Grab live FX prices from Yahoo & plot point by point
    #### till termination

    while True:
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        try:
            y = data_downloader.download_live_quote(vendor_ticker, 'Yahoo')
            s.write(dict(x = x, y = y))
        except: pass

        time.sleep(1)   # sleep for 1 second

if __name__ == '__main__':
    streaming_fx_study()
