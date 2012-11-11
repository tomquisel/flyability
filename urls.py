from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flyability.views.home', name='home'),
    url(r'^(?:flyability/)Brace$', 'siteviewer.views.shim'),
    url(r'^(?:flyability/)?sites/(?P<country>[^/]+)/(?P<state>[^/]+)/(?P<name>[^/]+)/?$', 'siteviewer.views.site'),
    url(r'^(?:flyability/)?sites/(?P<country>[^/]+)/(?P<state>[^/]+)/?$', 'siteviewer.views.state'),
    url(r'^(?:flyability/)?sites/(?P<country>[^/]+)/?$', 'siteviewer.views.country'),
    url(r'^(?:flyability/)?wind/dir_(?P<wind>[-\d]+)_(?P<left>\d+)_(?P<right>\d+)_(?P<size>\d+).png$', 'siteviewer.views.windDir'),
    url(r'^(?:flyability/)?wind/arrow_(?P<wind>[-\d]+)_(?P<left>\d+)_(?P<right>\d+)_(?P<size>\d+).png$', 'siteviewer.views.windArrow'),
    url(r'^(?:flyability/)?sites/allnames$', 'siteviewer.views.allSiteNames'),
    url(r'^(?:flyability/|/)?$', 'siteviewer.views.index'),
    url(r'^(?:flyability/|/)?search/?$', 'siteviewer.views.search'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'.*', 'fail'),
)
