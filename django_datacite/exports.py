from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .utils import get_settings


def export_resource(resource):
    data = {
        'schemaVersion': 'http://datacite.org/schema/kernel-4'
    }

    # identifiers
    if resource.identifier:
        data['identifiers'] = [{
            'identifier': resource.identifier.identifier,
            'identifierType': resource.identifier.identifier_type
        }]

    # creators
    creators = resource.creator_set.all()
    if creators:
        data['creators'] = [export_name(creator.name) for creator in creators]

    # titles
    titles = resource.titles.all()
    if titles:
        data['titles'] = [export_title(title) for title in titles]

    # publisher
    if resource.publisher:
        data['publisher'] = resource.publisher

    # publication_year
    if resource.publication_year is not None:
        data['publicationYear'] = str(resource.publication_year)

    # resource_type
    if resource.resource_type or resource.resource_type_general:
        data['types'] = {}
        if resource.resource_type:
            data['types']['resourceType'] = resource.resource_type
        if resource.resource_type_general:
            data['types']['resourceTypeGeneral'] = resource.resource_type_general

    # subjects
    subjects = resource.subjects.all()
    if subjects:
        data['subjects'] = [export_subject(subject) for subject in subjects]

    # contributors
    contributors = resource.contributor_set.all()
    if contributors:
        data['contributors'] = [export_name(contributor.name, contributor.contributor_type) for contributor in contributors]

    # dates
    dates = resource.dates.all()
    if dates:
        data['dates'] = [export_date(date) for date in dates]

    # language
    if resource.language:
        data['language'] = resource.language

    # alternate identifiers
    alternate_identifiers = resource.alternateidentifier_set.all()
    if alternate_identifiers:
        data['alternateIdentifiers'] = [{
            'alternateIdentifier': alternate_identifier.identifier.identifier,
            'alternateIdentifierType': alternate_identifier.identifier.identifier_type
        } for alternate_identifier in alternate_identifiers]

    # related identifiers
    related_identifiers = resource.relatedidentifier_set.all()
    if related_identifiers:
        data['relatedIdentifiers'] = [export_related_identifiers(related_identifier) for related_identifier in related_identifiers]

    # size
    if resource.size:
        data['size'] = resource.size

    # format
    if resource.format:
        data['format'] = resource.format

    # version
    if resource.version:
        data['version'] = resource.version

    # rights list
    rights_list = resource.rights_list.all()
    if rights_list:
        data['rightsList'] = [{
            'rights': rights.rights,
            'rightsURI':  rights.rights_uri,
            'rightsIdentifier': rights.rights_identifier,
            'rightsIdentifierScheme': rights.rights_identifier_scheme,
            'schemeURI': rights.scheme_uri,
        } for rights in rights_list]

    # descriptions
    descriptions = resource.descriptions.all()
    if descriptions:
        data['descriptions'] = [{
            'description': description.escaped_description,
            'descriptionType': description.description_type
        } for description in descriptions]

    # geo location
    geo_locations = resource.geo_locations.all()
    if geo_locations:
        data['geoLocations'] = [export_geo_location(geo_location) for geo_location in geo_locations]

    # funding reference
    funding_references = resource.fundingreference_set.all()
    if funding_references:
        data['fundingReferences'] = [export_funding_references(funding_reference) for funding_reference in funding_references]

    # related items
    related_items = resource.relateditem_set.all()
    if related_items:
        data['relatedItems'] = [export_related_item(related_item) for related_item in related_items]

    return data


def export_title(title):
    if title.title_type:
        return {'title': title.title, 'titleType': title.title_type}
    else:
        return {'title': title.title}


def export_name(name, contributor_type=None):
    data = {
        'name': name.name,
        'nameType': name.name_type
    }

    if contributor_type:
        data['contributorType'] = contributor_type

    if name.given_name:
        data['givenName'] = name.given_name

    if name.family_name:
        data['familyName'] = name.family_name

    name_identifiers = name.name_identifiers.all()
    if name_identifiers:
        data['nameIdentifiers'] = [{
            'nameIdentifier': name_identifier.name_identifier,
            'nameIdentifierScheme': name_identifier.name_identifier_scheme,
            'schemeURI': name_identifier.scheme_uri
        } for name_identifier in name_identifiers]

    affiliations = name.affiliations.all()
    if affiliations:
        data['affiliations'] = []
        for affiliation in affiliations:
            affiliation_name_identifier = affiliation.name_identifiers.first()
            if affiliation_name_identifier:
                data['affiliations'].append({
                    'affiliation': affiliation.name,
                    'affiliationIdentifier': affiliation_name_identifier.name_identifier,
                    'affiliationIdentifierScheme': affiliation_name_identifier.name_identifier_scheme,
                })
            else:
                data['affiliations'].append({
                    'affiliation': affiliation.name
                })

    return data


def export_subject(subject):
    data = {
        'subject': subject.subject
    }

    if subject.subject_scheme:
        data['subjectScheme'] = subject.subject_scheme

    if subject.subject_scheme:
        data['subjectScheme'] = subject.subject_scheme

    if subject.scheme_uri:
        data['schemeURI'] = subject.scheme_uri

    if subject.value_uri:
        data['valueURI'] = subject.value_uri

    if subject.classification_code:
        data['classificationCode'] = subject.classification_code

    return data


def export_date(date):
    data = {
        'date': date.date.isoformat(),
        'dateType': date.date_type
    }

    if date.date_information:
        data['dateInformation'] = date.date_information

    return data


def export_related_identifiers(related_identifier):
    data = {
        'relationType': related_identifier.relation_type,
        'relatedIdentifier': related_identifier.identifier.identifier,
        'relatedIdentifierType': related_identifier.identifier.identifier_type
    }

    # add DOI_BASE_URL to DOI
    if data['relatedIdentifierType'] == 'DOI' and not data['relatedIdentifier'].startswith('http'):
        data['relatedIdentifier'] = get_settings('DOI_BASE_URL') + data['relatedIdentifier']

    if getattr(settings, 'DATACITE_INCLUDE_CITATION', False):
        data['citation'] = related_identifier.identifier.citation

    return data


def export_geo_location(geo_location):
    data = {}

    if geo_location.geo_location_place:
        data['geoLocationPlace'] = geo_location.geo_location_place

    try:
        data['geoLocationPoint'] = {
            'pointLongitude': geo_location.geo_location_point.point_longitude,
            'pointLatitude': geo_location.geo_location_point.point_latitude
        }
    except ObjectDoesNotExist:
        pass

    try:
        data['geoLocationBox'] = {
            'westBoundLongitude': geo_location.geo_location_box.west_bound_longitude,
            'eastBoundLongitude': geo_location.geo_location_box.east_bound_longitude,
            'southBoundLatitude': geo_location.geo_location_box.south_bound_latitude,
            'northBoundLatitude': geo_location.geo_location_box.north_bound_latitude
        }
    except ObjectDoesNotExist:
        pass

    geo_location_polygons = []
    for geo_location_polygon in geo_location.geo_location_polygons.all():
        geo_location_polygons.append({
            'polygonPoints': [{
                'pointLongitude': polygon_point[0],
                'pointLatitude': polygon_point[1]
            } for polygon_point in geo_location_polygon.polygon_points],
            'inPolygonPoint': {
                'pointLongitude': geo_location_polygon.in_point_longitude,
                'pointLatitude': geo_location_polygon.in_point_latitude
            }
        })
    if geo_location_polygons:
        data['geoLocationPolygons'] = [geo_location_polygon for geo_location_polygon in geo_location_polygons]

    return data


def export_funding_references(funding_reference):
    data = {
        'funderName': funding_reference.funder.name
    }

    name_identifier = funding_reference.funder.name_identifiers.first()
    if name_identifier:
        data['funderIdentifier'] = name_identifier.name_identifier
        data['funderIdentifierType'] = name_identifier.name_identifier_scheme
        data['schemeURI'] = name_identifier.scheme_uri

    if funding_reference.award_number:
        data['awardNumber'] = funding_reference.award_number

    if funding_reference.award_uri:
        data['awardURI'] = funding_reference.award_uri

    if funding_reference.award_title:
        data['awardTitle'] = funding_reference.award_title

    return data


def export_related_item(related_item):
    data = {}

    # related_item_type
    if related_item.item.resource_type_general:
        data['relatedItemType'] = related_item.item.resource_type_general

    # related_item_type
    if related_item.relation_type:
        data['relationType'] = related_item.relation_type

    # related_item_identifier
    if related_item.item.identifier:
        data['relatedItemIdentifier'] = related_item.item.identifier.identifier
        data['relatedItemIdentifierType'] = related_item.item.identifier.identifier_type

    # creators
    creators = related_item.item.creator_set.all()
    if creators:
        data['creators'] = [export_name(creator.name) for creator in creators]

    # titles
    titles = related_item.item.titles.all()
    if titles:
        data['titles'] = [export_title(title) for title in titles]

    # publication_year
    if related_item.item.publication_year is not None:
        data['publicationYear'] = str(related_item.item.publication_year)

    # volume
    if related_item.volume:
        data['volume'] = related_item.volume

    # issue
    if related_item.issue:
        data['issue'] = related_item.issue

    # number
    if related_item.number:
        data['number'] = related_item.number

    # numberType
    if related_item.number_type:
        data['numberType'] = related_item.number_type

    # firstPage
    if related_item.first_page:
        data['firstPage'] = related_item.first_page

    # lastPage
    if related_item.last_page:
        data['lastPage'] = related_item.last_page

    # publisher
    if related_item.item.publisher:
        data['publisher'] = related_item.item.publisher

    # edition
    if related_item.edition:
        data['edition'] = related_item.edition

    # contributors
    contributors = related_item.item.contributor_set.all()
    if contributors:
        data['contributors'] = [export_name(contributor.name, contributor.contributor_type) for contributor in contributors]

    return data
