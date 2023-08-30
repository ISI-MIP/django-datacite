import json

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .exports import export_resource
from .models import Resource
from .renderers import XMLRenderer
from .utils import render_bibtex


def resource(request, identifier=None):
    resource = Resource.objects.filter(public=True, identifier__identifier=identifier).first()

    if resource:
        resource_url = reverse('django_datacite:resource', args=[resource.identifier.identifier])
        resource_xml_url = reverse('django_datacite:resource_xml', args=[resource.identifier.identifier])
        resource_json_url = reverse('django_datacite:resource_json', args=[resource.identifier.identifier])
        return render(request, 'datacite/resource.html', {
            'resource': resource,
            'resource_absolute_uri': request.build_absolute_uri(resource_url),
            'resource_xml_absolute_uri': request.build_absolute_uri(resource_xml_url),
            'resource_json_absolute_uri': request.build_absolute_uri(resource_json_url)
        })
    else:
        raise Http404


def resource_json(request, identifier=None):
    resource = Resource.objects.filter(public=True, identifier__identifier=identifier).first()
    if resource:
        resource_json = json.dumps(export_resource(resource), indent=2)
        response = HttpResponse(resource_json, content_type="application/json")
        response['Content-Disposition'] = f'filename="{resource.identifier}.json"'
        return response
    else:
        raise Http404


def resource_xml(request, identifier=None):
    resource = Resource.objects.filter(public=True, identifier__identifier=identifier).first()
    if resource:
        resource_xml = XMLRenderer().render(export_resource(resource))
        response = HttpResponse(resource_xml, content_type="application/xml")
        response['Content-Disposition'] = f'filename="{resource.identifier}.xml"'
        return response
    else:
        raise Http404


def resource_bibtex(request, identifier=None):
    resource = Resource.objects.filter(public=True, identifier__identifier=identifier).first()
    if resource:
        resource_bibtex = render_bibtex(resource)
        response = HttpResponse(resource_bibtex, content_type='application/x-bibtex')
        response['Content-Disposition'] = f'filename="{resource.identifier}.bib"'
        return response
    else:
        raise Http404
