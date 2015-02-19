from django.conf.urls import patterns, url

from api_docs.views import IPythonNotebookPage


urlpatterns = patterns(
    '',
    url("network-graphs/$",
        IPythonNotebookPage.as_view(
            lang='ipython-notebooks',
            notebook='networkx'),
        name='ipython-notebook-networkx'),
    url("subplots/$",
        IPythonNotebookPage.as_view(
            lang='ipython-notebooks',
            notebook='make_subplots'),
        name='ipython-notebook-make_subplots'),
    url("basemap-maps/$",
        IPythonNotebookPage.as_view(
            lang='ipython-notebooks',
            notebook='basemap'),
        name='ipython-notebook-basemap'),
    url("collaboration/$",
        IPythonNotebookPage.as_view(
            lang='ipython-notebooks',
            notebook='collaborate'),
        name='ipython-notebook-collaborate')
)
