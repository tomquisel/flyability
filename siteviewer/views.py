from siteviewer.models import Site
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

def site(request, name):
    site = get_object_or_404(Site, pk=name)
    return HttpResponse("Site: %s Alt: %s" % (site.name, site.altitude) )
