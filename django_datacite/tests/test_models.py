import pytest

from django.http import Http404

from django_datacite.models import GeoLocation, NameIdentifier, Resource

resource_id = 1
name_identifier_id = 1
geo_location_ids = [1, 2, 3]


def test_resource_get_absolute_url(db):
    resource = Resource.objects.get(id=resource_id)
    assert resource.get_absolute_url() == '/10.12345/12345'


def test_resource_get_absolute_url_404(db):
    resource = Resource.objects.get(id=resource_id)
    resource.identifier = None
    resource.save()

    with pytest.raises(Http404):
        resource.get_absolute_url()


def test_name_identifier_url(db):
    name_identifier = NameIdentifier.objects.get(id=name_identifier_id)
    assert name_identifier.url == 'https://ror.org/Eid1thua9'


@pytest.mark.parametrize('geo_location_id', geo_location_ids)
def test_geo_location_str(db, geo_location_id):
    geo_location = GeoLocation.objects.get(id=geo_location_id)
    assert str(geo_location)
