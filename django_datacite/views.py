import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from .models import Resource
from .renderers import XMLRenderer


def resource(request, identifier=None):
    return render(request, 'datacite/resource.html', {
        'resource': get_object_or_404(Resource.objects.all(), identifier__identifier=identifier)
    })


def resource_json(request, identifier=None):
    resource = get_object_or_404(Resource.objects.all(), identifier__identifier=identifier)
    response = HttpResponse(json.dumps(resource.serialize(), indent=2), content_type="application/json")
    response['Content-Disposition'] = 'filename="{}.json"'.format(identifier)
    return response


def resource_xml(request, identifier=None):
    resource = get_object_or_404(Resource.objects.all(), identifier__identifier=identifier)
    xml = XMLRenderer().render(resource.serialize())
    response = HttpResponse(xml, content_type="application/xml")
    response['Content-Disposition'] = 'filename="{}.xml"'.format(identifier)
    return response


def resource_bibtex(request, identifier=None):
    bibtex = render_to_string('datacite/resource.bib', {
        'resource': get_object_or_404(Resource.objects.all(), identifier__identifier=identifier)
    })
    # remove empty lines
    bibtex = '\n'.join([line for line in bibtex.splitlines() if line.strip()])
    response = HttpResponse(bibtex, content_type='application/x-bibtex')
    response['Content-Disposition'] = 'filename="{}.bib"'.format(identifier)
    return response
