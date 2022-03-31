from django.conf import settings
from django.template.loader import render_to_string

from . import settings as default_settings


def get_settings(key, default=None):
    if hasattr(settings, key):
        return getattr(settings, key)
    else:
        return getattr(default_settings, key, default)


def get_display_name(key, choices):
    try:
        return next(filter(lambda item: item[0] == key, choices))[1]
    except StopIteration:
        return None


def get_citation(resource):
    citation = render_to_string('datacite/citation.html', context={'resource': resource})
    return ' '.join(citation.split())


def serialize_resource(resource):
    data = {}

    # identifiers
    if resource.identifier:
        data['identifiers'] = [{
            'identifier': resource.identifier.identifier,
            'identifierType': resource.identifier.identifier_type
        }]

    # creators
    creators = resource.creator_set.order_by('order', 'name')
    if creators:
        data['creators'] = [serialize_name(creator.name) for creator in creators]

    # titles
    titles = resource.titles.all()
    if titles:
        data['titles'] = [serialize_title(title) for title in titles]

    # publisher
    if resource.publisher:
        data['publisher'] = resource.publisher

    # publication_year
    if resource.publication_year is not None:
        data['publicationYear'] = resource.publication_year

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
        data['subjects'] = [serialize_subject(subject) for subject in subjects]

    # contributors
    contributors = resource.contributor_set.order_by('order', 'name')
    if contributors:
        data['contributors'] = [serialize_name(contributor.name, contributor.contributor_type) for contributor in contributors]

    # dates
    dates = resource.dates.all()
    if dates:
        data['dates'] = [serialize_date(date) for date in dates]

    # language
    if resource.language:
        data['language'] = resource.language

    # alternate identifiers
    alternate_identifiers = resource.alternate_identifiers.all()
    if alternate_identifiers:
        data['alternateIdentifiers'] = [{
            'alternateIdentifier': alternate_identifier.identifier,
            'alternateIdentifierType': alternate_identifier.identifier_type
        } for alternate_identifier in alternate_identifiers]

    # related identifiers
    related_identifiers = resource.relatedidentifier_set.all()
    if related_identifiers:
        data['relatedIdentifiers'] = [serialize_related_identifiers(related_identifier) for related_identifier in related_identifiers]

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

    return data


def serialize_title(title):
    if title.title_type:
        return {'title': title.title, 'titleType': title.title_type}
    else:
        return {'title': title.title}


def serialize_name(name, contributor_type=None):
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


def serialize_subject(subject):
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


def serialize_date(date):
    data = {
        'date': date.date.isoformat(),
        'dateType': date.date_type
    }

    if date.date_information:
        data['dateInformation'] = date.date_information

    return data


def serialize_related_identifiers(related_identifier):
    data = {
        "relationType": related_identifier.relation_type,
        "relatedIdentifier": related_identifier.identifier.identifier,
        "relatedIdentifierType": related_identifier.identifier.identifier_type
    }

    if getattr(settings, 'DATACITE_INCLUDE_CITATION', False):
        data['citation'] = related_identifier.identifier.citation

    return data
