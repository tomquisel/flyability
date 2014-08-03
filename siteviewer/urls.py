from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('siteviewer.views',
    url(r'^$', 'index', name='index'),
    url(r'^search/?$', 'search', name='search'),
    url(r'^site/(?P<country>[^/]+)/(?P<state>[^/]+)/(?P<name>[^/]+)/?$', 
        'site', name='site'),
    url(r'^site/summary$', 'summary', name='summary'),
    url(r'^wind/dir_(?P<wind>[-\d]+)_(?P<siteid>\d+)_(?P<size>\d+).png$', 
        'windDir', name='windDir'),
    url(r'^sitelist$', 'sitelist', name='sitelist'),
    url(r'^setlevel$', 'setlevel', name='setlevel'),
)
