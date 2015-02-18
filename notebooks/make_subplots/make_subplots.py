
# coding: utf-8

# # Subplots and small multiples
# ## with plotly and `plotly.tools.make_subplots`

# In[1]:

from plotly import tools        # functions to help build plotly graphs
import plotly.plotly as py      # module that communicates with plotly 
from plotly.graph_objs import * # graph objects, subclasses of lists and dicts, that are used to describe plotly graphs


# #### Simple subplots

# In[2]:

fig = tools.make_subplots(rows=2)


# In[3]:

fig.append_trace(Scatter(x=[1,2,3], y=[2,1,2], name='top trace'), 1, 1)
fig.append_trace(Scatter(x=[1,2,3], y=[2,3,2], name='bottom trace'), 2, 1)
py.iplot(fig, filename='subplot example')


# #### Shared axes

# In[4]:

fig = tools.make_subplots(rows=2, shared_xaxes=True, print_grid=True)


# In[5]:

fig.append_trace(Scatter(x=[1,2,3], y=[2,1,2]), 1, 1)
fig.append_trace(Scatter(x=[2,3,4], y=[2,3,2]), 2, 1)
py.iplot(fig, filename='shared xaxis')


# ### loops

# In[6]:

nr = 6
nc = 6
fig = tools.make_subplots(rows=nr, cols=nc, print_grid=False)


# In[7]:

for i in range(1, nr+1):
    for j in range(1, nc+1):
        fig.append_trace(Scatter(x=[1], y=[1], 
                                 text=['({}, {})'.format(i,j)], 
                                 mode='markers+text',
                                 textposition='top'), row=i, col=j)

fig['layout']['showlegend'] = False
py.iplot(fig, filename='6x6')


# ### ... with shared axes

# In[8]:

nr = 6
nc = 6
fig = tools.make_subplots(rows=nr, cols=nc, print_grid=False,
                          shared_xaxes=True, shared_yaxes=True)


# In[9]:

for i in range(1, nr+1):
    for j in range(1, nc+1):
        fig.append_trace(Scatter(x=[1], y=[1], 
                                 text=['({}, {})'.format(i,j)], 
                                 mode='markers+text',
                                 textposition='top'), row=i, col=j)

fig['layout']['showlegend'] = False
py.iplot(fig, filename='6x6 shared')


# ### insets

# In[ ]:

fig = tools.make_subplots(insets=[{'cell': (1,1), 'l': 0.7, 'b': 0.7}],
                          print_grid=True)


# In[ ]:

fig.append_trace(Scatter(x=[1,2,3], y=[2,1,2]), 1, 1)
fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x2', yaxis='y2')]
py.iplot(fig, filename='inset example')


# ### spanning columns

# In[ ]:

fig = tools.make_subplots(rows=2, cols=2,
                          specs=[[{}, {}],
                                 [{'colspan': 2}, None]],
                          print_grid=True)


# In[ ]:

fig.append_trace(Scatter(x=[1,2,3], y=[2,1,2]), row=1, col=1)
fig.append_trace(Scatter(x=[1,2,3], y=[2,1,2]), row=1, col=2)
fig.append_trace(Scatter(x=[1,2,3], y=[2,1,2]), row=2, col=1)

py.iplot(fig, filename='irregular spacing')


# ### unique arrangements

# In[ ]:

fig = tools.make_subplots(rows=5, cols=2,
                          specs=[[{}, {'rowspan': 2}],
                                 [{}, None],
                                 [{'rowspan': 2, 'colspan': 2}, None],
                                 [None, None],
                                 [{}, {}]],
                          print_grid=True)


# In[ ]:

fig.append_trace(Scatter(x=[1,2],y=[1,4],name='(1,1)'),  1, 1)
fig.append_trace(Scatter(x=[1,2],y=[1,4],name='(2,1)'),  2, 1)
fig.append_trace(Scatter(x=[1,2],y=[1,4],name='(3,1)'),  3, 1)
fig.append_trace(Scatter(x=[1,2],y=[1,4],name='(5,1)'),  5, 1)

fig.append_trace(Scatter(x=[1,2],y=[1,4],name='(1,2)'),  1, 2)
fig.append_trace(Scatter(x=[1,2],y=[1,4],name='(5,2)'),  5, 2)

py.iplot(fig, filename='subplot unique arrangement')


# ### walkthrough

# `tools.make_subplots` *generates* `Figure` objects for you.
# 
# Need some help? Call `help`

# In[ ]:

help(tools.make_subplots)


# In[ ]:

fig = tools.make_subplots(rows=2)


# `fig` is a subclass of a `dict`

# In[ ]:

print fig


# `to.string()` pretty prints the object

# In[ ]:

print fig.to_string()


# `fig` subclasses a `dict`, so access members just like you would in a `dict`

# In[ ]:

fig['layout']


# it's a bit different than a straight dictionary because only certain keys are allowed.
# 
# each key and value describes something about a plotly graph, so it's pretty strict.
# 
# for example, you can't initialize a `Figure` with an invalid key. we'll throw an exception.

# In[ ]:

import traceback
try:
    Figure(nonsense=3)
except:
    print traceback.format_exc()


# so, which keys are accepted? call `help`! also check out [https://plot.ly/python/reference/](https://plot.ly/python/reference/)

# In[ ]:

help(fig['layout'])


# In[ ]:

fig['layout']['title'] = 'two subplots'


# `fig.append_trace` is a helper function for binding trace objects to axes. need some help? call `help`!

# In[ ]:

help(fig.append_trace)


# In[ ]:

fig.append_trace(Scatter(x=[1,2,3], y=[2,1,2], name='top trace'), row=1, col=1) # (row, col) match with the subplot arrangment that was printed out
fig.append_trace(Scatter(x=[1,2,3], y=[2,1,2], name='bottom trace'), row=2, col=1)
print fig


# In[ ]:

print fig.to_string()


# see the two Scatter traces in `fig['data']` above? we just inserted those!
# 
# to view this graph, send it over to your plotly account

# In[ ]:

py.iplot(fig, filename='subplot example')


# now take a look at the examples above. in each case, we're just specifying a subplot arrangment and appending traces to the subplot coordinates that were printed
# 

# ### Questions? <support@plot.ly>, [@plotlygraphs](https://twitter.com/plotlygraphs)
