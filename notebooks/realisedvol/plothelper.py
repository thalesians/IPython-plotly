__author__ = 'saeedamen'

"""
    Thalesians Ltd (www.thalesians.com) please contact saeed@pythalesians.com for further information
    You are free to modify and distribute this code as you see fit provided this source is cited
"""

# for dates
import datetime

# for plotting data
import plotly
from plotly.graph_objs import *

class PlotHelper:
    def parse_dates(self, str_dates):
        # parse_dates - parses string dates into Python format
        #
        # str_dates = dates to be parsed in the format of day/month/year
        #

        dates = []

        for d in str_dates:
            dates.append(datetime.datetime.strptime(d, '%d/%m/%Y'))

        return dates

    def convert_df_plotly(self, dataframe, axis_no = 1, color_def = ['default'],
                          special_line = 'Mean', showlegend = True, addmarker = False, gradcolor = None):
        # convert_df_plotly - converts a Pandas data frame to Plotly format for line plots
        # dataframe = data frame due to be converted
        # axis_no = axis for plot to be drawn (default = 1)
        # special_line = make lines named this extra thick
        # color_def = color scheme to be used (default = ['default']), colour will alternate in the list
        # showlegend = True or False to show legend of this line on plot
        # addmarker = True or False to add markers
        # gradcolor = Create a graduated color scheme for the lines
        #
        # Also see http://nbviewer.ipython.org/gist/nipunreddevil/7734529 for converting dataframe to traces
        # Also see http://moderndata.plot.ly/color-scales-in-ipython-notebook/

        x = dataframe.index

        traces = []

        # will be used for market opacity for the markers
        increments = 0.95 / float(len(dataframe.columns))

        if gradcolor is not None:
            try:
                import colorlover as cl
                color_def = cl.scales[str(len(dataframe.columns))]['seq'][gradcolor]
            except:
                print('Check colorlover installation...')

        i = 0

        for key in dataframe:
            scatter = plotly.graph_objs.Scatter(
                        x = x,
                        y = dataframe[key].values,
                        name = key,
                        xaxis = 'x' + str(axis_no),
                        yaxis = 'y' + str(axis_no),
                        showlegend = showlegend)

            # only apply color/marker properties if not "default"
            if color_def[i % len(color_def)] != "default":
                if special_line in str(key):
                    # special case for lines labelled "mean"
                    # make line thicker
                    scatter['mode'] = 'lines'
                    scatter['line'] = plotly.graph_objs.Line(
                                color = color_def[i % len(color_def)],
                                width = 2
                            )

                else:
                    line_width = 1

                    # set properties for the markers which change opacity
                    # for markers make lines thinner
                    if addmarker:
                        opacity = 0.05 + (increments * i);
                        scatter['mode'] = 'markers+lines'
                        scatter['marker'] = plotly.graph_objs.Marker(
                                    color=color_def[i % len(color_def)],  # marker color
                                    opacity = opacity,
                                    size = 5)
                        line_width = 0.2

                    else:
                        scatter['mode'] = 'lines'

                    scatter['line'] = plotly.graph_objs.Line(
                            color = color_def[i % len(color_def)],
                            width = line_width)

                i = i + 1

            traces.append(scatter)

        return traces

    def create_layout(self, title, xaxis, yaxis, width = -1, height = -1):
        # create_layout - populates a layout object
        # title = title of the plot
        # xaxis = xaxis label
        # yaxis = yaxis label
        # width (optional) = width of plot
        # height (optional) = height of plot
        #

        layout = Layout(
                    title = title,
                    xaxis = plotly.graph_objs.XAxis(
                        title = xaxis,
                        showgrid = False
                ),
                    yaxis = plotly.graph_objs.YAxis(
                        title= yaxis,
                        showline = False
                )
            )

        if width > 0 and height > 0:
            layout['width'] = width
            layout['height'] = height

        return layout


     # def convert_df_plotly_heatmap(self, dataframe, colorscale = 'black'):
     #    # convert_df_plotly_heatmap - converts a Pandas data frame to Plotly format for heatmap
     #    # dataframe = data frame due to be converted
     #    # color_def = color scheme to be used (default = ['default'])
     #    #
     #    # Also see http://nbviewer.ipython.org/gist/nipunreddevil/7734529
     #    #
     #
     #    x = []; y = []
     #
     #    for i in dataframe.columns.values:
     #        y.append(str(i))
     #
     #    for i in dataframe.index.values:
     #        x.append(str(i))
     #
     #    return plotly.graph_objs.Heatmap(
     #                    z = numpy.transpose(dataframe.values),
     #                    x = x,
     #                    y = y,
     #                    colorscale = colorscale)

    # def largest(self, spot, number, ascending = True):
    #     # largest - calculates the top (or bottom) values of an asset
    #     #
    #     # spot = price of asset to study
    #     # ascending = boolean whether to sort ascending or descending
    #     #
    #
    #     spot = spot.sort(columns = spot.columns[0], ascending = ascending)
    #
    #     return spot.head(n = number)

    # def plot_vol_surface(self):
    #     # plot FX volatility surface
    #     if source == 'Bloomberg':
    #         req = egthalesians.plotly.bbg_com.ReferenceDataRequest('GBPUSD Curncy', 'DFLT_VOL_SURF_MID')
    #         req.execute()
    #
    #         vol_surface = req.response.values[:,0][0]
    #
    #         data = Data([plotly.graph_objs.Surface(
    #             z =[ vol_surface['Maturity'],
    #                  vol_surface['Delta'],
    #                  vol_surface['Volatility']])])
    #
    #         # data = Data([plotly.graph_objs.Scatter3d(
    #         #     x = vol_surface['Maturity as Percent of Year'],
    #         #     y = vol_surface['Delta'],
    #         #     z = vol_surface['Volatility'])])
    #
    #         layout = Layout(
    #             title='GBPUSD FX Implied Volatility Surface',
    #             autosize=False,
    #         )
    #
    #         fig = Figure(data=data, layout=layout)
    #         plot_url = py.plot(fig, filename='gbpusd-implied-vol-surface')





