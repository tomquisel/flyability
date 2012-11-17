from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('siteviewer.views',
    # Examples:
    url(r'^flyability/?$', 'index', name='index'),
    url(r'^flyability/search/?$', 'search', name='search'),
    url(r'^flyability/sites/(?P<country>[^/]+)/(?P<state>[^/]+)/(?P<name>[^/]+)/?$', 
        'site', name='site'),
    url(r'^flyability/wind/dir_(?P<wind>[-\d]+)_(?P<siteid>\d+)_(?P<size>\d+).png$', 
        'windDir', name='windDir'),
    url(r'^flyability/Brace$', 'shim'),

    # unused
    #url(r'^flyability/wind/arrow_(?P<wind>[-\d]+)_(?P<left>\d+)_(?P<right>\d+)_(?P<size>\d+).png$', 'windArrow'),
    #url(r'^flyability/sites/(?P<country>[^/]+)/(?P<state>[^/]+)/?$', 'state'),
    #url(r'^flyability/sites/(?P<country>[^/]+)/?$', 'country'),
    #url(r'^flyability/sites/allnames$', 'allSiteNames'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
