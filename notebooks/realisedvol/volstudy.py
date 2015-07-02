__author__ = 'saeedamen'

"""
    Thalesians Ltd (www.pythalesians.com) please contact saeed@pythalesians.com for further information
    You are free to modify and distribute this code as you see fit provided this source is cited
"""
# for time series/maths
import pandas
import math
import datetime
from datetime import timedelta

# for plotting data
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

# for data downloading
from datadownloader import DataDownloader

# for event analysis/plotting
from plothelper import PlotHelper

postfix = "test" # what to put at the end of the Plotly URL

def vol_study():
    # Learn about API authentication here: https://plot.ly/python/getting-started
    # Find your api_key here: https://plot.ly/settings/api
    plotly_username = "thalesians"
    plotly_api_key = "XXXXX"

    plotly.tools.set_credentials_file(username = plotly_username, api_key = plotly_api_key)

    ticker = 'EURUSD' # will use in plot titles later (and for creating Plotly URL)

    ##### Download intraday EUR/USD data from Bloomberg or CSV file
    source = "Bloomberg"
    source = "CSV"

    csv_file = None

    plot_helper = PlotHelper()

    data_downloader = DataDownloader()
    start_date = datetime.datetime.utcnow() - timedelta(days = 120)
    freq = 'intraday'

    if source == 'Bloomberg':
        vendor_ticker = 'EURUSD BGN Curncy'
    elif source == 'CSV':
        vendor_ticker = 'EURUSD'
        csv_file = 'D:/EURUSD.csv'

    spot = data_downloader.download_time_series(vendor_ticker, ticker, start_date, source, csv_file = csv_file, freq = freq)

    #### Calculate 1 day realised vol on EUR/USD data from Bloomberg using different data frequency (1 min, ..., 60 min)
    minute_freq = [1, 5, 10, 30, 60]

    realised_vol = None

    for min in minute_freq:
        spot_min = spot.loc[spot.index.minute % min == 0]
        rets = spot_min / spot_min.shift(1) - 1
        realised_vol_min = pandas.rolling_std(rets, 1440.0 / min) * math.sqrt(252.0 * (1440.0 / min)) * 100
        realised_vol_min.columns = [str(min) + 'min']
        if realised_vol is None: realised_vol = realised_vol_min
        else:
            realised_vol = realised_vol.join(realised_vol_min, how = 'outer')

    # reduce the number of points to plot
    realised_vol = realised_vol.loc[realised_vol.index.minute % 60 == 0]

    xaxis = 'Date'
    yaxis = 'Daily Realised Vol'
    source_label = "Source: @thalesians/BBG"

    # Using varying shades of blue for each line (helped by colorlover library)

    title = ticker + ' Realised Vol 1D Window' + '<BR>' + source_label
    realised_vol.index = pandas.to_datetime(realised_vol.index.values)

    # also apply graduated color scheme of blues (from light to dark)
    # see http://moderndata.plot.ly/color-scales-in-ipython-notebook/ for details on colorlover package
    # which allows you to set scales
    fig = Figure(data = plot_helper.convert_df_plotly(realised_vol, gradcolor = 'Blues', addmarker=False),
                 layout = plot_helper.create_layout(title, xaxis, yaxis),
    )

    filename = 'realised-vol-freq-' + str(ticker) + str(postfix)
    plot_url = py.iplot(fig, filename = filename)

    #### Calculate Realised Vol on S&P500 data from Yahoo and compare with VIX index
    source = 'Yahoo'

    start_date = datetime.datetime.utcnow() - timedelta(days = 365)
    spx = data_downloader.download_time_series('^GSPC', 'S&P500', start_date, source)
    vix = data_downloader.download_time_series('^VIX', 'VIX', start_date, source)

    # calculate realised vol on S&P500 (and shift it to be aligned to VIX - implied vol)
    spx_realised_vol = pandas.rolling_std(spx / spx.shift(1) - 1, 20) * math.sqrt(252) * 100
    spx_realised_vol = spx_realised_vol.shift(-20)

    vol = spx_realised_vol.join(vix, how = 'outer')

    source_label = "Source: @thalesians/Yahoo"
    title = "Comparing S&P500 1M realised vol with VIX" + '<BR>' + source_label
    xaxis = 'Date'
    yaxis = 'Vol'

    fig = Figure(data = plot_helper.convert_df_plotly(vol, addmarker = True),
                 layout = plot_helper.create_layout(title, xaxis, yaxis),
    )

    plot_url = py.iplot(fig, filename = 'sp500-vix-comparison-' + str(postfix))

if __name__ == '__main__':
    vol_study()
