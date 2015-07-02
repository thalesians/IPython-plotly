__author__ = 'saeedamen'

"""
    Thalesians Ltd (www.pythalesians.com) please contact saeed@pythalesians.com for further information
    You are free to modify and distribute this code as you see fit provided this source is cited
"""

# for time series manipulation
import pandas
import pandas.io.data as web

import datetime

class DataDownloader:
    def download_live_quote(self, vendor_ticker, source):
        if source == 'Yahoo':
            from urllib2 import urlopen
            response = urlopen('http://finance.yahoo.com/d/quotes.csv?s=' + vendor_ticker + '&f=sl1d1t1c1ohgv&e=.csv')
            html = response.read()

            split = html.split(",")

            price = split[1]

        return price

    def download_time_series(self, vendor_ticker, pretty_ticker, start_date, source, csv_file = None,
                             freq = 'daily', freq_no = 1):
        if not(isinstance(start_date, list)):
            start_date = [start_date]

        if freq == 'daily':
            if source == 'Quandl':
                import Quandl
                # Quandl requires API key for large number of daily downloads
                # https://www.quandl.com/help/api
                spot = Quandl.get(vendor_ticker)    # Bank of England's database on Quandl
                spot = pandas.DataFrame(data = spot['Value'], index = spot.index)
                spot.columns = [pretty_ticker]
            elif source == 'Yahoo':
                finish_date = datetime.datetime.utcnow()
                finish_date = datetime.datetime(finish_date.year, finish_date.month, finish_date.day, 0, 0, 0)

                spot = web.DataReader(vendor_ticker, 'yahoo', start_date[0], finish_date)
                spot = pandas.DataFrame(data = spot['Close'].values, index = spot.index, columns = [pretty_ticker])

                spot.index = pandas.DatetimeIndex(spot.index)

            elif source == 'Bloomberg':
                from egthalesians.plotly.helper.bbg_com import HistoricalDataRequest
                req = HistoricalDataRequest([vendor_ticker], ['PX_LAST'], start = start_date[0])
                req.execute()

                spot = req.response_as_single()
                spot.columns = [pretty_ticker]
            elif source == 'CSV':
                dateparse = lambda x: pandas.datetime.strptime(x, '%Y-%m-%d')

                # in case you want to use a source other than Bloomberg/Quandl
                spot = pandas.read_csv(csv_file, index_col=0, parse_dates=0, date_parser=dateparse)

        elif freq == 'intraday':
            if source == 'Bloomberg':
                from egthalesians.plotly.helper.bbg_com import IntrdayBarRequest
                req = IntrdayBarRequest(vendor_ticker, freq_no, start = start_date[0])

                req.execute()

                spot = req.response
                spot.columns = [pretty_ticker + '.' + x for x in spot.columns]

                spot = pandas.DataFrame(data = spot[pretty_ticker + ".close"].values,
                                        index = spot.index, columns = [pretty_ticker + ".close"])

            elif source == 'CSV':
                dateparse = lambda x: pandas.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

                # in case you want to use a source other than Bloomberg/Quandl etc
                try:
                    spot = pandas.read_csv(csv_file, index_col = 0, parse_dates = 0, date_parser = dateparse)
                except:
                    dateparse = lambda x: pandas.datetime.strptime(x, '%d/%m/%Y %H:%M:%S')
                    spot = pandas.read_csv(csv_file, index_col = 0, parse_dates = 0, date_parser = dateparse)

        return spot