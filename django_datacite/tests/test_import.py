import json

from django.conf import settings

from django_datacite.imports import import_resource
from django_datacite.models import Identifier, Name, Resource, Subject

resource_id = 1


def test_import(db):
    file_path = settings.BASE_PATH / 'json' / 'resource.json'
    with open(file_path, encoding='utf8') as fp:
        file_data = json.load(fp)

    resource = Resource()
    resource = import_resource(resource, file_data)


def test_import_blank(db):
    file_path = settings.BASE_PATH / 'json' / 'resource.json'
    with open(file_path, encoding='utf8') as fp:
        file_data = json.load(fp)

    Resource.objects.all().delete()
    Name.objects.all().delete()
    Identifier.objects.all().delete()
    Subject.objects.all().delete()

    resource = Resource()
    resource = import_resource(resource, file_data)


def test_import_resource(db):
    file_path = settings.BASE_PATH / 'json' / 'resource.json'
    with open(file_path, encoding='utf8') as fp:
        file_data = json.load(fp)

    resource = Resource.objects.get(id=resource_id)
    resource = import_resource(resource, file_data)
