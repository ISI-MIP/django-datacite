from django.urls import reverse


def test_resource(db, client):
    response = client.get(reverse('datacite:resource', args=['10.12345/12345']))
    assert response.status_code == 200


def test_resource_error(db, client):
    response = client.get(reverse('datacite:resource', args=['10.12345/00000']))
    assert response.status_code == 404


def test_resource_json(db, client):
    response = client.get(reverse('datacite:resource_json', args=['10.12345/12345']))
    assert response.status_code == 200


def test_resource_json_error(db, client):
    response = client.get(reverse('datacite:resource_json', args=['10.12345/00000']))
    assert response.status_code == 404


def test_resource_xml(db, client):
    response = client.get(reverse('datacite:resource_xml', args=['10.12345/12345']))
    assert response.status_code == 200


def test_resource_xml_error(db, client):
    response = client.get(reverse('datacite:resource_xml', args=['10.12345/00000']))
    assert response.status_code == 404


def test_resource_bibtex(db, client):
    response = client.get(reverse('datacite:resource_bibtex', args=['10.12345/12345']))
    assert response.status_code == 200


def test_resource_bibtex_error(db, client):
    response = client.get(reverse('datacite:resource_bibtex', args=['10.12345/00000']))
    assert response.status_code == 404
