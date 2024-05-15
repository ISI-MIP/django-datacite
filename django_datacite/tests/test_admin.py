import json
import re

from django.conf import settings
from django.urls import reverse

from django_datacite.models import Resource

resource_id = 1
name_id = 1
identifier_id = 1
subject_id = 1


def test_resource_changelist_get(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_changelist')
    response = client.get(url)
    assert response.status_code == 200


def test_resource_change_get(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_change', args=[resource_id])
    response = client.get(url)
    assert response.status_code == 200


def test_resource_add_post(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_add')
    response = client.post(url, {
        '_save': 'Save',
        'titles-TOTAL_FORMS': 0,
        'titles-INITIAL_FORMS': 0,
        'titles-MIN_NUM_FORMS': 0,
        'titles-MAX_NUM_FORMS': 1000,
        'descriptions-TOTAL_FORMS': 0,
        'descriptions-INITIAL_FORMS': 0,
        'descriptions-MIN_NUM_FORMS': 0,
        'descriptions-MAX_NUM_FORMS': 1000,
        'creator_set-TOTAL_FORMS': 0,
        'creator_set-INITIAL_FORMS': 0,
        'creator_set-MIN_NUM_FORMS': 0,
        'creator_set-MAX_NUM_FORMS': 1000,
        'contributor_set-TOTAL_FORMS': 0,
        'contributor_set-INITIAL_FORMS': 0,
        'contributor_set-MIN_NUM_FORMS': 0,
        'contributor_set-MAX_NUM_FORMS': 1000,
        'dates-TOTAL_FORMS': 0,
        'dates-INITIAL_FORMS': 0,
        'dates-MIN_NUM_FORMS': 0,
        'dates-MAX_NUM_FORMS': 1000,
        'alternateidentifier_set-TOTAL_FORMS': 0,
        'alternateidentifier_set-INITIAL_FORMS': 0,
        'alternateidentifier_set-MIN_NUM_FORMS': 0,
        'alternateidentifier_set-MAX_NUM_FORMS': 1000,
        'relatedidentifier_set-TOTAL_FORMS': 0,
        'relatedidentifier_set-INITIAL_FORMS': 0,
        'relatedidentifier_set-MIN_NUM_FORMS': 0,
        'relatedidentifier_set-MAX_NUM_FORMS': 1000,
        'Resource_subjects-TOTAL_FORMS': 0,
        'Resource_subjects-INITIAL_FORMS': 0,
        'Resource_subjects-MIN_NUM_FORMS': 0,
        'Resource_subjects-MAX_NUM_FORMS': 1000,
        'rights_list-TOTAL_FORMS': 0,
        'rights_list-INITIAL_FORMS': 0,
        'rights_list-MIN_NUM_FORMS': 0,
        'rights_list-MAX_NUM_FORMS': 1000,
        'Resource_geo_locations-TOTAL_FORMS': 0,
        'Resource_geo_locations-INITIAL_FORMS': 0,
        'Resource_geo_locations-MIN_NUM_FORMS': 0,
        'Resource_geo_locations-MAX_NUM_FORMS': 1000,
        'fundingreference_set-TOTAL_FORMS': 0,
        'fundingreference_set-INITIAL_FORMS': 0,
        'fundingreference_set-MIN_NUM_FORMS': 0,
        'fundingreference_set-MAX_NUM_FORMS': 1000,
        'relateditem_set-TOTAL_FORMS': 0,
        'relateditem_set-INITIAL_FORMS': 0,
        'relateditem_set-MIN_NUM_FORMS': 0,
        'relateditem_set-MAX_NUM_FORMS': 1000
    })
    assert response.status_code == 302
    assert response.url == '/admin/datacite/resource/'


def test_resource_export_get_json(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_export', args=[resource_id, 'json'])
    response = client.get(url)
    assert response.status_code == 200


def test_resource_export_get_xml(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_export', args=[resource_id, 'xml'])
    response = client.get(url)
    assert response.status_code == 200


def test_resource_export_get_bibtex(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_export', args=[resource_id, 'bibtex'])
    response = client.get(url)
    assert response.status_code == 200


def test_resource_export_get_404(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_export', args=[1000, 'json'])
    response = client.get(url)
    assert response.status_code == 404


def test_resource_export_get_404_format(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_export', args=[resource_id, 'error'])
    response = client.get(url)
    assert response.status_code == 404


def test_resource_import_get(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import')
    response = client.get(url)
    assert response.status_code == 200


def test_resource_import_post_file(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import')
    file_path = settings.BASE_PATH / 'json' / 'resource.json'
    with open(file_path, encoding='utf8') as fp:
        response = client.post(url, {'_send': True, 'file': fp})
    assert response.status_code == 302
    assert re.search(r'/admin/datacite/resource/\d+/change/', response.url)


def test_resource_import_post_file_invalid(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import')
    file_path = settings.BASE_PATH / 'json' / 'invalid.json'
    with open(file_path, encoding='utf8') as fp:
        response = client.post(url, {'_send': True, 'file': fp})
    assert response.status_code == 200


def test_resource_import_post_url(db, client, requests_mock):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import')
    file_path = settings.BASE_PATH / 'json' / 'resource.json'
    with open(file_path, encoding='utf8') as fp:
        requests_mock.get('https://example.com/datacite.json', json=json.load(fp))

    response = client.post(url, {'_send': True, 'url': 'https://example.com/datacite.json'})
    assert response.status_code == 302
    assert re.search(r'/admin/datacite/resource/\d+/change/', response.url)


def test_resource_import_post_url_invalid(db, client, requests_mock):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import')
    file_path = settings.BASE_PATH / 'json' / 'invalid.json'
    with open(file_path, encoding='utf8') as fp:
        requests_mock.get('https://example.com/datacite.json', text=fp.read())

    response = client.post(url, {'_send': True, 'url': 'https://example.com/datacite.json'})
    assert response.status_code == 200


def test_resource_import_post_file_url(db, client, requests_mock):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import')
    file_path = settings.BASE_PATH / 'json' / 'resource.json'
    with open(file_path, encoding='utf8') as fp:
        response = client.post(url, {'_send': True, 'file': fp, 'url': 'https://example.com/datacite.json'})
    assert response.status_code == 200


def test_resource_import_post_none(db, client, requests_mock):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import')
    response = client.post(url, {'_send': True})
    assert response.status_code == 200


def test_resource_import_post_back(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import')
    response = client.post(url, {'_back': True})
    assert response.status_code == 302
    assert response.url == '/admin/datacite/resource/'


def test_resource_import_resource_get(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import', args=[resource_id])
    response = client.get(url)
    assert response.status_code == 200


def test_resource_import_resource_post(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import', args=[resource_id])
    file_path = settings.BASE_PATH / 'json' / 'resource.json'
    with open(file_path, encoding='utf8') as fp:
        response = client.post(url, {'_send': True, 'file': fp})
    assert response.status_code == 302
    assert response.url == '/admin/datacite/resource/1/change/'


def test_resource_import_resource_post_back(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_import', args=[resource_id])
    response = client.post(url, {'_back': True})
    assert response.status_code == 302
    assert response.url == '/admin/datacite/resource/1/change/'


def test_resource_copy_get(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_copy', args=[resource_id])
    response = client.get(url)
    assert response.status_code == 200


def test_resource_copy_post(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_copy', args=[resource_id])
    response = client.post(url, {'_send': True})
    assert response.status_code == 302
    assert Resource.objects.count() == 3


def test_resource_copy_post_back(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_copy', args=[resource_id])
    response = client.post(url, {'_back': True})
    assert response.status_code == 302
    assert Resource.objects.count() == 2


def test_resource_create_new_version_get(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_create_new_version', args=[resource_id])
    response = client.get(url)
    assert response.status_code == 200


def test_resource_create_new_version_post(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_create_new_version', args=[resource_id])
    response = client.post(url, {'_send': True})
    assert response.status_code == 302
    assert Resource.objects.count() == 3


def test_resource_create_new_version_post_back(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_create_new_version', args=[resource_id])
    response = client.post(url, {'_back': True})
    assert response.status_code == 302
    assert Resource.objects.count() == 2


def test_resource_validate_get(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_resource_validate', args=[resource_id])
    response = client.get(url)
    assert response.status_code == 200


def test_name_change_get(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_name_change', args=[name_id])
    response = client.get(url)
    assert response.status_code == 200


def test_identifier_change_get(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_identifier_change', args=[identifier_id])
    response = client.get(url)
    assert response.status_code == 200


def test_subject_change_get(db, client):
    client.login(username='admin', password='admin')

    url = reverse('admin:datacite_subject_change', args=[subject_id])
    response = client.get(url)
    assert response.status_code == 200
