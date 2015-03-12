
# coding: utf-8

# In[29]:

from IPython.display import Image


# In[31]:

Image('http://i.imgur.com/SYija2N.png')


# ###### Download your Gmail inbox as a ".mbox" file by clicking on "Account" under your Gmail user menu, then "Download data"

# ###### Install the Python libraries mailbox and dateutils with <code>sudo pip install mailbox</code> and <code>sudo pip install dateutils</code>

# In[12]:

import mailbox
from email.utils import parsedate
from dateutil.parser import parse
import itertools
import plotly.plotly as py
from plotly.graph_objs import *


# In[13]:

path = '/Users/jack/Desktop/All mail Including Spam and Trash.mbox'


# ##### Open your ".mbox" file with <code>mailbox</code>

# In[22]:

mbox = mailbox.mbox(path)


# ##### Sort your mailbox by date

# In[23]:

def extract_date(email):
    date = email.get('Date')
    return parsedate(date)

sorted_mails = sorted(mbox, key=extract_date)
mbox.update(enumerate(sorted_mails))
mbox.flush()


# ##### Organize dates of email receipt as a list

# In[24]:

all_dates = []
mbox = mailbox.mbox(path)
for message in mbox:
    all_dates.append( str( parse( message['date'] ) ).split(' ')[0] )


# ##### Count and graph emails received per day

# In[25]:

email_count = [(g[0], len(list(g[1]))) for g in itertools.groupby(all_dates)]


# In[26]:

email_count[0]


# In[27]:

x = []
y = []
for date, count in email_count:
    x.append(date)
    y.append(count)


# In[28]:

py.iplot( Data([ Scatter( x=x, y=y ) ]) )


# ##### Restyle the chart in Plotly's GUI

# In[10]:

import plotly.tools as tls
tls.embed('https://plot.ly/~jackp/3266')

