
# coding: utf-8

# In[1]:

import networkx as nx

import plotly.plotly as py
from plotly.graph_objs import *


# In[2]:

G=nx.random_geometric_graph(200,0.125)


# In[3]:

# add the edges in as disconnected lines in a single trace
edge_trace = Scatter(x=[], y=[], mode='lines')
for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

# add the nodes in as a scatter
node_trace = Scatter(x=[], y=[], mode='markers', marker=Marker(size=[]))
for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)

# size the node points by the number of connections
for node, adjacencies in enumerate(G.adjacency_list()):
    node_trace['marker']['size'].append(len(adjacencies))


# In[4]:

# create a figure so we can customize a couple more things
fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(title='random geometric graph from networkx', plot_bgcolor="rgb(217, 217, 217)",
                           showlegend=False, xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

# send the figure to Plotly and embed an iframe in this notebook
py.iplot(fig, filename='networkx')

