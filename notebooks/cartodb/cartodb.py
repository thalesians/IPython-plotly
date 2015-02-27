
# coding: utf-8

#### <div style="margin: auto; width: 800px; display: block;"> <img src="https://plot.ly/static/learn/images/plotly-hist-logo.png" style="width: 200px; display: inline;" /> <span style="font-size: 5em;">+</a> <img src="http://cartodb.s3.amazonaws.com/static/logos_full_cartodb_light.png" style="width: 350px; display: inline;" /></div>

# [CartoDB](http://cartodb.com/) lets you easily make web-based maps driven by a PostgreSQL/PostGIS backend, so data management is easy. [Plotly](https://plot.ly) is a cloud-based graphing and analytics platform with [Python, R, & MATLAB APIs](https://plot.ly/api) where collaboration is easy. This IPython Notebook shows how to use them together to analyze earthquake data.

# In[1]:

# Import needed libraries
get_ipython().magic(u'pylab inline')
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.tools as tls


# **Getting started**
# 
# 1. Setup a free CartoDB account at [https://cartodb.com/signup](https://cartodb.com/signup) or use data linked in this notebook
# 2. Use Plotly's sandbox account, or [sign-up](https://plot.ly/python/getting-started/). No downloads required.

# In[2]:

py.sign_in('Python-Demo-Account', 'gwt101uhh0')


# Pandas's [`read_csv`](http://pandas.pydata.org/pandas-docs/dev/generated/pandas.io.parsers.read_csv.html) allows import via HTTP, FTP, etc. It's perfect for CartoDB's [SQL API](), which has the following template:
# ```
# http://{account_name}.cartodb.com/api/v2/sql?q={custom_sql_statement}&format=csv
# ```
# 
# To get data from the data table in my CartoDB account, the following query grabs values we can graph, and converts the timestamp to work easily with plotly.
# 
# ```sql
# SELECT
#    mag,
#    magtype,
#    type,
#    to_char(time,'yyyy-mm-DD HH24:MI:SS') AS time_plotly,
#    place,
#    depth
# FROM
#   all_month
# ```
# 
# All we need to do is replace the white space with `%20` so the URL is properly encoded.

# In[3]:

url = "http://andye.cartodb.com/api/v2/sql?"      "q=SELECT%20mag,magtype,type,to_char(time,'yyyy-mm-DD%20HH24:MI:SS')%20AS%20time_plotly,place,depth%20FROM%20all_month"      "&format=csv"
df = pd.read_csv(url)
df = df.sort(['mag'], ascending=[0]);


# In[4]:

df.head()


# Let's take a look at the magnitude in a histogram. 

# In[5]:

mag_histogram_plot = [{'x': df['mag'], 
                 'type': 'histogram'
}]


# In[6]:

data_histogram = Data(mag_histogram_plot)

fig_histogram = Figure(data=data_histogram)


# In[7]:

py.iplot(fig_histogram, filename='magnitude_histogram')


# Let's check out the same data in a box plot. 

# In[8]:

mag_jitter_plot = [{'y': df['mag'], 
                 'name': 'Earthquake Magnitude',
                 'type': 'box',
                 'boxpoints': 'outliers', 
                 'jitter': 0.9,
}]


# In[9]:

data_jitter = Data(mag_jitter_plot)

fig_jitter = Figure(data=data_jitter)


# In[10]:

py.iplot(fig_jitter, filename='boxplot_with_jitter')


# If we want to put the plot in a report, email, or presentation we can export the static version. The plot URL contains the data, code to reproduce the plot with MATLAB, R, and Python, and can be embedded. 
# <br>
# <br>
# <br>
# - https://plot.ly/~Python-Demo-Account/1534.png
# - https://plot.ly/~Python-Demo-Account/1534.svg
# - https://plot.ly/~Python-Demo-Account/1534.pdf
# - https://plot.ly/~Python-Demo-Account/1534.eps
# - https://plot.ly/~Python-Demo-Account/1534.m
# - https://plot.ly/~Python-Demo-Account/1534.py
# - https://plot.ly/~Python-Demo-Account/1534.r
# - https://plot.ly/~Python-Demo-Account/1534.jl
# - https://plot.ly/~Python-Demo-Account/1534.json
# - https://plot.ly/~Python-Demo-Account/1534.embed
# <br>
# <br>
# <br>
# You and others you share the plot with can also collaborate and style the plot in the GUI. 
# <br>
# <br>
# <br>
# <img src="http://i.imgur.com/Cwtea9h.gif" /></a>
# <br>
# <br>
# <br>

# Let's take another pass at it, and this time put both magnitude and depth in the same plot. 

# In[11]:

location = df['place']  # manages serialization in early versions of Plotly Python client
for i in range(len(location)):
    try:
        location[i] = str(location[i]).decode('utf-8')
    except:
        location[i] = 'Country name decode error'


# In[12]:

trace1 = Scatter(
    x=df['depth'],
    y=df['mag'],
    text=location,
    mode='markers',
    marker=Marker(
            color='rgba(31, 119, 180, 0.15)',  # add opacity for visibility
        )
)
layout = Layout(
    title='Earthquake Magnitude vs. Depth',
    xaxis=XAxis( type='log', title='depth' ),
    yaxis=YAxis( type='log', title='magnitude' ),
    hovermode="closest",
)
data = Data([trace1])
fig = Figure(data=data, layout=layout)
py.iplot(fig, filename='Earthquake_basic')


# If you click and drag, you can zoom in on the plot. Hover your mouse to see data about each earthquake. Now, for our final plot, we can make a scatter plot over time, showing the magnitude on the y axis with the point sized for depth. 

# In[13]:

depth_time_plot = [Scatter({'y': df['mag'], 
               'x': df['time_plotly'],
               'name': 'Earthquake Depth',
               'mode': 'markers',
               'text': df['place'],
               'marker': {
                    'size': 20.0 * (df['depth'] + abs(df['depth'].min())) / (df['depth'].max() + abs(df['depth'].min()))
                }})]


# In[14]:

data_depth = Data(depth_time_plot)

layout_depth = Layout(yaxis=YAxis(title='Magnitude of the Event'),xaxis=XAxis(title='Date of Event'),hovermode='closest')

fig_depth = Figure(data=data_depth, layout=layout_depth )


# In[15]:

py.iplot(fig_depth)


# Moving over to CartoDB, you can import the data table into your account by copying the following URL and pasting it into the [CartoDB Importer](http://docs.cartodb.com/cartodb-editor.html#importing-data):
# 
#     http://andye.cartodb.com/api/v2/sql?q=SELECT%20*%20FROM%20all_month&format=csv&filename=earthquake_data_plotly
# 
# This just uses the CartoDB [SQL API](http://docs.cartodb.com/cartodb-platform/sql-api.html) again, with the additional parameter `filename` that specifices the name of the datatable on import.
# 
# By selecting the Torque in the [Visualization Wizard](http://docs.cartodb.com/cartodb-editor.html#wizards) you can get an animated map of the earthquakes over time. Make sure to select the `time` column in the wizard. By clicking on the `CSS` tab, you can customize your map further. Copy &amp; Past the CartoCSS below the map to reproduce it's style.

# In[4]:

from IPython.display import HTML
HTML('<iframe width=100% height=520 frameborder=0 src=https://andye.cartodb.com/viz/e44ac140-b8ad-11e4-b156-0e4fddd5de28/embed_map allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen></iframe>')


# ```css
# /** Torque visualization */
# Map {
# -torque-frame-count:512;
# -torque-animation-duration:30;
# -torque-time-attribute:"time";
# -torque-aggregation-function:"max(mag)";
# -torque-resolution:2;
# -torque-data-aggregation:linear;
# }
# 
# #earthquake_data_plotly{
#   comp-op: lighter;
#   marker-fill-opacity: 0.9;
#   marker-line-color: #FFF;
#   marker-line-width: 0;
#   marker-line-opacity: 1;
#   marker-type: ellipse;
#   marker-width: 6;
#   marker-fill: #3E7BB6;
# }
# 
# #earthquake_data_plotly[value >7] {
#   marker-width: 20;
#   marker-fill: #3e7bb6;
#   [frame-offset=1] {
#     marker-width:19;
#     marker-fill-opacity:0.8;
#   }
#   [frame-offset=2] {
#     marker-width:18;
#     marker-fill-opacity:0.7; 
#   }
#   [frame-offset=3] {
#     marker-width:17;
#     marker-fill-opacity:0.6; 
#   }
#   [frame-offset=4] {
#     marker-width:16;
#     marker-fill-opacity:0.5; 
#   }
#   [frame-offset=5] {
#     marker-width:15;
#     marker-fill-opacity:0.4;
#   }
# }
# 
# #earthquake_data_plotly[value<=7][value>6] {
#   marker-width: 16;
#   marker-fill: #C3CEFF;
#   [frame-offset=1] {
#     marker-width:14;
#     marker-fill-opacity:0.7;
#   }
#   [frame-offset=2] {
#     marker-width:13;
#     marker-fill-opacity:0.6; 
#   }
#   [frame-offset=3] {
#     marker-width:12;
#     marker-fill-opacity:0.5; 
#   }
#   [frame-offset=4] {
#     marker-width:11;
#     marker-fill-opacity:0.4; 
#   }
# }
# 
# #earthquake_data_plotly[value<=6][value>5] {
#   marker-width: 12;
#   marker-fill: #FFFFFF;
#   [frame-offset=1] {
#     marker-width:10;
#     marker-fill-opacity:0.6;
#   }
#   [frame-offset=2] {
#     marker-width:8;
#     marker-fill-opacity:0.5; 
#   }
#   [frame-offset=3] {
#     marker-width:6;
#     marker-fill-opacity:0.4;
#   }
# }
# 
# #earthquake_data_plotly[value<=5][value>4] {
#   marker-width: 6;
#   marker-fill: yellow; 
#   [frame-offset=1] {
#     marker-width:4;
#     marker-fill-opacity:0.5;
#   }
#   [frame-offset=2] {
#     marker-width:2;
#     marker-fill-opacity:0.4;
#   }
# }
# 
# #earthquake_data_plotly[value <= 4][value > 3] {
#   marker-width: 3;
#   marker-fill: orange;
#   [frame-offset=1] {
#     marker-width:2;
#     marker-fill-opacity:0.4;
#   }
#   [frame-offset=2] {
#     marker-width:1;
#     marker-fill-opacity:0.3;
#   }
# }
# 
# #earthquake_data_plotly[value <= 3][value > 2] {
#   marker-width: 2;
#   marker-fill: red;
#   [frame-offset=1] {
#     marker-width:1.5;
#     marker-fill-opacity:0.3;
#   }
#   [frame-offset=2] {
#     marker-width:1;
#     marker-fill-opacity:0.2;
#   }
# }
# 
# #earthquake_data_plotly[value <= 2] {
#   marker-fill: #850200;
#   marker-width: 0.5;
#   [frame-offset=1] {
#     marker-width:0;
#     marker-fill-opacity:0;
#   }
# }
# ```
