from django.urls import re_path

from django_datacite.views import resource, resource_bibtex, resource_json, resource_xml

app_name = 'django_datacite'

urlpatterns = [
    re_path(r'^(?P<identifier>\d{2}\.\d+\/[A-Za-z0-9_.\-\/]+).xml$', resource_xml, name='resource_xml'),
    re_path(r'^(?P<identifier>\d{2}\.\d+\/[A-Za-z0-9_.\-\/]+).json$', resource_json, name='resource_json'),
    re_path(r'^(?P<identifier>\d{2}\.\d+\/[A-Za-z0-9_.\-\/]+).bib$', resource_bibtex, name='resource_bibtex'),
    re_path(r'^(?P<identifier>\d{2}\.\d+\/[A-Za-z0-9_.\-\/]+)', resource, name='resource')
]
