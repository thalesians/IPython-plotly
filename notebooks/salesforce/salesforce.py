
# coding: utf-8

# # Interactive Salesforce Graphing
# 
# Salesforce reports are great for getting a handle on the numbers but [Plotly](http://plot.ly/) allows for interactivity not built into the Reports Module in Salesforce. Luckily Salesforce has amazing tools around exporting data, from excel and csv files to a robust and reliable API. With [Simple Salesforce](https://github.com/neworganizing/simple-salesforce), it's simple to make REST calls to the Salesforce API and get your hands on data to make real time, interactive dashboards.
# 
# This notebook walks you through that basic process of getting something like that set up. 
# 
# First you'll need [Plotly](http://plot.ly/). Plotly is a free web-based platform for making graphs. You can keep graphs private, make them public, and run Plotly on your own servers (https://plot.ly/product/enterprise/). To get started visit https://plot.ly/python/getting-started/ . It's simple interface makes it easy to get interactive graphics done quickly.
# 
# You'll also need a Salesforce Developer (or regular Salesforce Account). [You can get a salesforce developer account for free](https://developer.salesforce.com/signup) at their developer portal.

# In[1]:

# we'll first start off with some basic imports.
import pandas as pd
import numpy as np
from collections import Counter
import requests

import plotly.plotly as py
from plotly.graph_objs import *

from simple_salesforce import Salesforce
requests.packages.urllib3.disable_warnings() # this squashes insecure SSL warnings - DO NOT DO THIS ON PRODUCTION!


# I've stored my Salesforce login in a text file however you're free to store them as environmental variables. As a reminder, login details should NEVER be included in version control.

# Logging into Salesforce is as easy as entering in your username, password, and security token given to you by Salesforce.
# 
# [Here's how to get your security token from Salesforce.](https://help.salesforce.com/apex/HTViewHelpDoc?id=user_security_token.htm)

# In[2]:

with open('salesforce_login.txt') as f:
    username, password, token = [x.strip("\n") for x in f.readlines()]
sf = Salesforce(username=username, password=password, security_token=token)


# At this time we're going to write a simply SOQL query to get some basic information from some leads. We'll query the status and Owner from our leads.
# 
# Further reference for the Salesforce API and writing SOQL queries:
# 
# http://www.salesforce.com/us/developer/docs/soql_sosl/
# 
# SOQL is just Salesforce's version of SQL.

# In[3]:

leads_for_status = sf.query("SELECT Id, Status, Owner.Name FROM Lead")


# Now we'll use a quick list comprehension to get just our statuses from those records (which are in an ordered dictionary format).

# In[4]:

statuses = [x['Status'] for x in leads_for_status["records"]]
status_counts = Counter(statuses)


# Now we can take advantage of Plotly's simple IPython Notebook interface to plot the graph in our notebook.

# In[5]:

data = Data([Bar(x=status_counts.keys(), y=status_counts.values())])
py.iplot(data, filename='salesforce/lead-distributions')


# While this graph gives us a great overview what status our leads are in, we'll likely want to know how each of the sales representatives are doing with their own leads. For that we'll need to get the owners using a similar list comprehension as we did above for the status.

# In[6]:

owners = [x['Owner']['Name'] for x in leads_for_status["records"]]


# For simplicity in grouping the values, I'm going to plug them into a pandas DataFrame.

# In[7]:

df = pd.DataFrame({'Owners':owners, 'Status':statuses})


# Now that we've got that we can do a simple lead comparison to compare how our Sales Reps are doing with their leads. We just create the bars for each lead owner.

# In[8]:

lead_comparison = []
for name, vals in df.groupby('Owners'):
    counts = vals.Status.value_counts()
    lead_comparison.append(Bar(x=counts.index, y=counts.values, name=name))


# In[9]:

py.iplot(Data(lead_comparison), filename='salesforce/lead-owner-status-groupings')


# What's great is that plotly makes it simple to compare across groups. However now that we've seen leads, it's worth it to look into Opportunities.

# In[10]:

opportunity_amounts = sf.query("SELECT Id, Probability, StageName, Amount, Owner.Name FROM Opportunity WHERE AMOUNT < 10000")


# In[11]:

amounts = [x['Amount'] for x in opportunity_amounts['records']]
owners = [x['Owner']['Name'] for x in opportunity_amounts['records']]


# In[12]:

hist1 = Histogram(x=amounts)


# In[13]:

py.iplot(Data([hist1]), filename='salesforce/opportunity-probability-histogram')


# In[14]:

df2 = pd.DataFrame({'Amounts':amounts,'Owners':owners})


# In[15]:

opportunity_comparisons = []
for name, vals in df2.groupby('Owners'):
    temp = Histogram(x=vals['Amounts'], opacity=0.75, name=name)
    opportunity_comparisons.append(temp)


# In[16]:

layout = Layout(
    barmode='stack'
)
fig = Figure(data=Data(opportunity_comparisons), layout=layout)


# In[17]:

py.iplot(fig, filename='salesforce/opportunities-histogram')


# By clicking on the "play with this data!" you can export, share, collaborate, and embed these plots. I've used it to share annotations about data and try out more colors. The GUI makes it easy for less technically oriented people to play with the data as well. Check out how the above was changed below or you can follow the link to make your own edits.

# In[18]:

from IPython.display import HTML
HTML("""<div>
    <a href="https://plot.ly/~bill_chambers/21/" target="_blank" title="Chuck vs Bill Sales Amounts" style="display: block; text-align: center;"><img src="https://plot.ly/~bill_chambers/21.png" alt="Chuck vs Bill Sales Amounts" style="max-width: 100%;width: 1368px;"  width="1368" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="bill_chambers:21" src="https://plot.ly/embed.js" async></script>
</div>""")


# After comparing those two representatives. It's always helpful to have that high level view of the sales pipeline. Below I'm querying all of our open opportunities with their Probabilities and close dates. This will help us make a forecasting graph of what's to come soon.

# In[19]:

large_opps = sf.query("SELECT Id, Name, Probability, ExpectedRevenue, StageName, Amount, CloseDate, Owner.Name FROM Opportunity WHERE StageName NOT IN ('Closed Lost', 'Closed Won') AND Amount > 5000")


# In[20]:

large_opps_df = pd.DataFrame(large_opps['records'])
large_opps_df['Owner'] = large_opps_df.Owner.apply(lambda x: x['Name']) # just extract owner name
large_opps_df.drop('attributes', inplace=True, axis=1) # get rid of extra return data from Salesforce
large_opps_df.head()


# In[21]:

scatters = []
for name, temp_df in large_opps_df.groupby('Owner'):
    hover_text = temp_df.Name + "<br>Close Probability: " + temp_df.Probability.map(str) + "<br>Stage:" + temp_df.StageName
    scatters.append(
        Scatter(
            x=temp_df.CloseDate,
            y=temp_df.Amount,
            mode='markers',
            name=name,
            text=hover_text,
            marker=Marker(
                size=(temp_df.Probability / 2) # helps keep the bubbles of managable size
            )
        )
    )


# In[22]:

data = Data(scatters)
layout = Layout(
    title='Open Large Deals',
    xaxis=XAxis(
        title='Close Date'
    ),
    yaxis=YAxis(
        title='Deal Amount',
        showgrid=False
    )
)
fig = Figure(data=data, layout=layout)
py.iplot(fig, filename='salesforce/open-large-deals-scatter')

