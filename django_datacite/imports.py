import logging
import os

from django.utils.dateparse import parse_date

from .models import (AlternateIdentifier, Contributor, Creator, Date,
                     Description, FundingReference, GeoLocation,
                     GeoLocationBox, GeoLocationPoint, GeoLocationPolygon,
                     Identifier, Name, NameIdentifier, RelatedIdentifier,
                     RelatedItem, Resource, Rights, Subject, Title)
from .utils import get_settings

logger = logging.getLogger(__name__)


def import_resource(resource_instance, data):
    # identifier and identifierType
    identifier_nodes = data.get('identifiers', [])
    if identifier_nodes and isinstance(identifier_nodes, list) and len(identifier_nodes) == 1:
        resource_instance.identifier = import_identifier(identifier_nodes[0])

    # publisher
    publisher = data.get('publisher')
    if publisher:
        resource_instance.publisher = publisher

    # publicationYear
    publication_year = data.get('publicationYear')
    if publication_year is not None:
        resource_instance.publication_year = publication_year

    # resourceType and resourceTypeGeneral
    types_node = data.get('types')
    if types_node and isinstance(types_node, dict):
        resource_type = types_node.get('resourceType')
        if resource_type:
            resource_instance.resource_type = resource_type

        resource_type_general = types_node.get('resourceTypeGeneral')
        if Resource.validate_resource_type_general(resource_type_general):
            resource_instance.resource_type_general = resource_type_general

    # language
    language = data.get('language')
    if language and Resource.validate_language(language):
        resource_instance.language = language

    # size
    size = data.get('size')
    if size is not None:
        resource_instance.size = size

    # format
    format = data.get('format')
    if format is not None:
        resource_instance.format = format

    # version
    version = data.get('version')
    if version is not None:
        resource_instance.version = version

    # save here so the import of the related fields work as expected
    resource_instance.save()

    # titles
    title_nodes = data.get('titles')
    if title_nodes and isinstance(title_nodes, list):
        for title_node in title_nodes:
            title = title_node.get('title')
            title_type = title_node.get('titleType', '')
            if title and Title.validate_title_type(title_type):
                title_instance, created = Title.objects.update_or_create(
                    resource=resource_instance,
                    title_type=title_node.get('titleType', ''),
                    defaults={
                        'title': title
                    }
                )
                logger.info('Title="%s" %s', title_instance, 'created' if created else 'updated')

    # creators
    creator_nodes = data.get('creators')
    if creator_nodes and isinstance(creator_nodes, list):
        for order, creator_node in enumerate(creator_nodes):
            name_instance = import_name(creator_node)
            if name_instance:
                creator_instance, created = Creator.objects.update_or_create(
                    resource=resource_instance,
                    name=name_instance,
                    defaults={
                        'order': order
                    }
                )
                logger.info('Creator="%s" %s', creator_instance, 'created' if created else 'updated')

    # titles
    description_nodes = data.get('descriptions')
    if description_nodes and isinstance(description_nodes, list):
        for description_node in description_nodes:
            description_type = description_node.get('descriptionType')
            if Description.validate_description_type(description_type):
                description_instance, created = Description.objects.update_or_create(
                    resource=resource_instance,
                    description_type=description_type,
                    defaults={
                        'description': description_node.get('description', '')
                                                       .replace('<br>', os.linesep + os.linesep)
                    }
                )
                logger.info('Description="%s" %s', description_instance, 'created' if created else 'updated')

    # contributors
    contributors_nodes = data.get('contributors')
    if contributors_nodes and isinstance(contributors_nodes, list):
        for order, contributor_node in enumerate(contributors_nodes):
            contributor_type = contributor_node.get('contributorType')
            if Contributor.validate_contributor_type(contributor_type):
                name_instance = import_name(contributor_node)
                if name_instance:
                    contributor_instance, created = Contributor.objects.update_or_create(
                        resource=resource_instance,
                        name=name_instance,
                        defaults={
                            'order': order,
                            'contributor_type': contributor_type
                        }
                    )
                    logger.info('Contributor="%s" %s', contributor_instance, 'created' if created else 'updated')

    # subjects
    subject_nodes = data.get('subjects')
    if subject_nodes and isinstance(subject_nodes, list):
        for subject_node in subject_nodes:
            subject_instance = import_subject(subject_node)
            resource_instance.subjects.add(subject_instance)

    # dates
    date_nodes = data.get('dates')
    if date_nodes and isinstance(date_nodes, list):
        for date_node in date_nodes:
            date = parse_date(date_node.get('date'))
            date_type = date_node.get('dateType')
            if date is not None and Date.validate_date_type(date_type):
                date_instance, created = Date.objects.update_or_create(
                    resource=resource_instance,
                    date_type=date_node.get('dateType'),
                    defaults={
                        'date': date,
                        'date_information': date_node.get('dateInformation', '')
                    }
                )
                logger.info('Date="%s" %s', date_instance, 'created' if created else 'updated')

    # alternateIdentifiers
    alternate_identifier_nodes = data.get('alternateIdentifiers')
    if alternate_identifier_nodes and isinstance(alternate_identifier_nodes, list):
        for order, alternate_identifier_node in enumerate(alternate_identifier_nodes):
            identifier_instance = import_identifier({
                'identifier': alternate_identifier_node.get('alternateIdentifier'),
                'identifierType': alternate_identifier_node.get('alternateIdentifierType'),
                'citation': alternate_identifier_node.get('citation', '')
            })

            if identifier_instance is not None:
                alternate_identifier_instance, created = AlternateIdentifier.objects.update_or_create(
                    resource=resource_instance,
                    identifier=identifier_instance,
                    defaults={
                        'order': order
                    }
                )
                logger.info('AlternateIdentifier="%s" %s', alternate_identifier_instance, 'created' if created else 'updated')

    # relatedIdentifiers
    related_identifier_nodes = data.get('relatedIdentifiers')
    if related_identifier_nodes and isinstance(related_identifier_nodes, list):
        for order, related_identifier_node in enumerate(related_identifier_nodes):
            relation_type = related_identifier_node.get('relationType')
            resource_type_general = related_identifier_node.get('resourceTypeGeneral')

            if RelatedIdentifier.validate_relation_type(relation_type):
                identifier_instance = import_identifier({
                    'identifier': related_identifier_node.get('relatedIdentifier'),
                    'identifierType': related_identifier_node.get('relatedIdentifierType'),
                    'citation': related_identifier_node.get('citation', '')
                })

                if identifier_instance is not None:
                    resource_type_general = related_identifier_node.get('resourceTypeGeneral')
                    if not RelatedIdentifier.validate_resource_type_general(resource_type_general):
                        resource_type_general = RelatedIdentifier.get_default_resource_type_general()

                    related_identifier_instance, created = RelatedIdentifier.objects.update_or_create(
                        resource=resource_instance,
                        identifier=identifier_instance,
                        defaults={
                            'order': order,
                            'relation_type': relation_type,
                            'resource_type_general': resource_type_general
                        }
                    )
                    logger.info('RelatedIdentifier="%s" %s', related_identifier_instance, 'created' if created else 'updated')

    # rightsList
    right_list_node = data.get('rightsList')
    if right_list_node and isinstance(right_list_node, list):
        for right_node in right_list_node:
            # look for the rightsIdentifier
            rights_identifier = right_node.get('rightsIdentifier')
            if rights_identifier is None:
                # if its not there, look for the rightsIdentifier
                rights_uri = right_node.get('rightsURI')
                rights_identifier = Rights.get_rights_identifier_by_uri(rights_uri)

            if rights_identifier:
                rights_instance, created = Rights.objects.update_or_create(
                    resource=resource_instance,
                    rights_identifier=rights_identifier
                )
                logger.info('Rights="%s" %s', rights_instance, 'created' if created else 'updated')

    # geoLocations
    geo_locations_node = data.get('geoLocations')
    if geo_locations_node and isinstance(geo_locations_node, list):
        for geo_location_node in geo_locations_node:
            geo_location_instance = import_geo_location(geo_location_node)
            resource_instance.geo_locations.add(geo_location_instance)

    # funding_references
    funding_reference_nodes = data.get('fundingReferences')
    if funding_reference_nodes and isinstance(funding_reference_nodes, list):
        for funding_reference_node in funding_reference_nodes:
            funder_instance = import_name({
                'name': funding_reference_node.get('funderName'),
                'nameType': Name.get_affiliation_name_type(),
                'nameIdentifiers': [
                    {
                        'nameIdentifier': funding_reference_node.get('funderIdentifier'),
                        'nameIdentifierScheme': funding_reference_node.get('funderIdentifierType')
                    }
                ]
            })
            if name_instance:
                funding_reference_instance, created = FundingReference.objects.update_or_create(
                    resource=resource_instance,
                    funder=funder_instance,
                    defaults={
                        'award_number': funding_reference_node.get('awardNumber', ''),
                        'award_uri': funding_reference_node.get('awardURI', ''),
                        'award_title': funding_reference_node.get('awardTitle', '')
                    }
                )
                logger.info('FundingReference="%s" %s', funding_reference_instance, 'created' if created else 'updated')

    # related_items
    related_item_nodes = data.get('relatedItems')
    if related_item_nodes and isinstance(related_item_nodes, list):
        for related_item_node in related_item_nodes:
            identifier = related_item_node.get('relatedItemIdentifier')
            identifier_type = related_item_node.get('relatedItemIdentifierType')

            # try to find the related item as existing resource in the database
            try:
                item_instance = Resource.objects.get(
                    identifier__identifier=identifier,
                    identifier__identifier_type=identifier_type
                )
            except Resource.DoesNotExist:
                item_instance = Resource()

            # create or update the related item resource
            item_instance = import_resource(item_instance, {
                'types': {
                    'resourceTypeGeneral': related_item_node.get('relatedItemType')
                },
                'identifiers': [{
                    'identifier': identifier,
                    'identifierType': identifier_type
                }],
                'creators': related_item_node.get('creators'),
                'titles': related_item_node.get('titles'),
                'publicationYear': related_item_node.get('publicationYear'),
                'publisher': related_item_node.get('publisher'),
                'contributors': related_item_node.get('contributors')
            })

            number_type = related_item_node.get('numberType')
            if not RelatedItem.validate_number_type(number_type):
                number_type = RelatedItem.get_default_number_type()

            related_item_instance, created = RelatedItem.objects.update_or_create(
                resource=resource_instance,
                item=item_instance,
                defaults={
                    'relation_type': related_item_node.get('relationType', ''),
                    'volume': related_item_node.get('volume', ''),
                    'issue': related_item_node.get('issue', ''),
                    'number': related_item_node.get('number', ''),
                    'number_type': number_type,
                    'first_page': related_item_node.get('firstPage', ''),
                    'last_page': related_item_node.get('lastPage', ''),
                    'edition': related_item_node.get('edition', ''),
                }
            )
            logger.info('RelatedItem="%s" %s', related_item_instance, 'created' if created else 'updated')

    return resource_instance


def import_identifier(identifier_node):
    identifier = identifier_node.get('identifier')
    identifier_type = identifier_node.get('identifierType')

    if identifier_type == 'DOI':
        identifier = identifier.replace(get_settings('DOI_BASE_URL'), '')

    if identifier and Identifier.validate_identifier_type(identifier_type):
        identifier_instance, created = Identifier.objects.update_or_create(
            identifier=identifier,
            identifier_type=identifier_type
        )

        if created:
            # set citation only when the instance is initially created
            identifier_instance.citation = identifier_node.get('citation', '')
            identifier_instance.save()

        logger.info('Identifier="%s" %s', identifier_instance, 'created' if created else 'updated')
        return identifier_instance


def import_name(name_node):
    # search for name identifiers
    name_identifier_instances = []
    name_identifier_nodes = name_node.get('nameIdentifiers')
    if name_identifier_nodes and isinstance(name_identifier_nodes, list):
        for name_identifier_node in name_identifier_nodes:
            name_identifier = name_identifier_node.get('nameIdentifier')
            name_identifier_scheme = name_identifier_node.get('nameIdentifierScheme')
            if name_identifier and NameIdentifier.validate_name_identifier_scheme(name_identifier_scheme):
                try:
                    name_identifier_instance = NameIdentifier.objects.get(
                        name_identifier=name_identifier,
                        name_identifier_scheme=name_identifier_scheme
                    )
                    logger.info('NameIdentifier="%s" found', name_identifier_instance)
                except NameIdentifier.DoesNotExist:
                    name_identifier_instance = NameIdentifier(
                        name_identifier=name_identifier,
                        name_identifier_scheme=name_identifier_scheme
                    )
                    logger.info('NameIdentifier="%s" created', name_identifier_instance)
                name_identifier_instances.append(name_identifier_instance)

    # search for affiliations
    affiliation_instances = []
    affiliation_nodes = name_node.get('affiliations')
    if affiliation_nodes and isinstance(affiliation_nodes, list):
        for affiliation_node in affiliation_nodes:
            affiliation_name = affiliation_node.get('affiliation')
            affiliation_name_identifier = affiliation_node.get('affiliationIdentifier')
            affiliation_name_identifier_scheme = affiliation_node.get('affiliationIdentifierScheme')

            if affiliation_name or (
                affiliation_name_identifier and
                NameIdentifier.validate_name_identifier_scheme(affiliation_name_identifier_scheme)
            ):
                affiliation_instance = import_name({
                    'name': affiliation_name,
                    'nameType': Name.get_affiliation_name_type(),
                    'nameIdentifiers': [
                        {
                            'nameIdentifier': affiliation_name_identifier,
                            'nameIdentifierScheme': affiliation_name_identifier_scheme
                        }
                    ]
                })

                if affiliation_instance:
                    affiliation_instances.append(affiliation_instance)

    # find (using the name_identifier_instances or the exact name) or create name
    name = name_node.get('name')
    given_name = name_node.get('givenName')
    family_name = name_node.get('familyName')
    try:
        name_instance = Name.objects.get(name_identifiers__in=name_identifier_instances)
        logger.info('Name="%s" found by NameIdentifier', name_instance)
    except Name.DoesNotExist:
        if name is None:
            if given_name and family_name:
                name = f'{given_name} {family_name}'
            else:
                return

        try:
            name_instance = Name.objects.get(name=name)
            logger.info('Name="%s" found by Name', name_instance)
        except Name.DoesNotExist:
            name_type = name_node.get('nameType', Name.get_default_name_type())
            if not Name.validate_name_type(name_type):
                return

            name_instance = Name(name=name, name_type=name_type,
                                 given_name=given_name or '', family_name=family_name or '')
            name_instance.save()
            logger.info('Name="%s" created', name_instance)

    # update name identifiers
    for name_identifier_instance in name_identifier_instances:
        try:
            name_identifier_instance.name
        except Name.DoesNotExist:
            name_identifier_instance.name = name_instance
            name_identifier_instance.save()

    # update affiliations
    name_instance.affiliations.set(affiliation_instances)

    return name_instance


def import_subject(subject_node):
    subject_instance = None

    subject = subject_node.get('subject')
    scheme_uri = subject_node.get('schemeURI', '')
    value_uri = subject_node.get('valueURI', '')

    if scheme_uri and value_uri:
        try:
            subject_instance = Subject.objects.get(
                scheme_uri=scheme_uri,
                value_uri=value_uri
            )
            logger.info('Subject="%s" found', subject_instance)
        except Subject.DoesNotExist:
            pass

    if subject_instance is None:

        try:
            subject_instance = Subject.objects.get(
                subject=subject
            )
            logger.info('Subject="%s" found', subject_instance)
        except Subject.DoesNotExist:
            pass

    if subject_instance is None:
        subject_instance = Subject.objects.create(
            subject=subject,
            subject_scheme=subject_node.get('subjectScheme', ''),
            scheme_uri=scheme_uri,
            value_uri=value_uri,
            classification_code=subject_node.get('classificationCode', ''),

        )
        logger.info('Subject="%s" created', subject_instance)

    return subject_instance


def import_geo_location(geo_location_node):
    geo_location_instance, created = GeoLocation.objects.update_or_create(
        geo_location_place=geo_location_node.get('geoLocationPlace', '')
    )
    logger.info('GeoLocation="%s" %s', geo_location_instance, 'created' if created else 'updated')

    geo_location_point = geo_location_node.get('geoLocationPoint')
    if geo_location_point and \
            geo_location_point.get('pointLongitude') is not None and \
            geo_location_point.get('pointLatitude') is not None:
        geo_location_point_instance, created = GeoLocationPoint.objects.update_or_create(
            geo_location=geo_location_instance,
            defaults={
                'point_longitude': geo_location_point.get('pointLongitude'),
                'point_latitude': geo_location_point.get('pointLatitude')
            }
        )

    geo_location_bbox = geo_location_node.get('geoLocationBox')
    if geo_location_bbox and \
            geo_location_bbox.get('westBoundLongitude') is not None and \
            geo_location_bbox.get('eastBoundLongitude') is not None and \
            geo_location_bbox.get('southBoundLatitude') is not None and \
            geo_location_bbox.get('northBoundLatitude') is not None:
        geo_location_bbox_instance, created = GeoLocationBox.objects.update_or_create(
            geo_location=geo_location_instance,
            defaults={
                'west_bound_longitude': geo_location_bbox.get('westBoundLongitude'),
                'east_bound_longitude': geo_location_bbox.get('eastBoundLongitude'),
                'south_bound_latitude': geo_location_bbox.get('southBoundLatitude'),
                'north_bound_latitude': geo_location_bbox.get('northBoundLatitude')
            }
        )

    geo_location_polygons = geo_location_node.get('geoLocationPolygons', [])
    for geo_location_polygon in geo_location_polygons:
        polygon_points = geo_location_polygon.get('polygonPoints')
        if polygon_points:
            polygon_points_json = [
                [point.get('pointLongitude'), point.get('pointLatitude')]
                for point in polygon_points
            ]
            geo_location_polygon_instance, created = GeoLocationPolygon.objects.update_or_create(
                geo_location=geo_location_instance,
                polygon_points=polygon_points_json,
                in_point_longitude=geo_location_polygon.get('inPolygonPoint', {}).get('pointLongitude'),
                in_point_latitude=geo_location_polygon.get('inPolygonPoint', {}).get('pointLatitude')
            )

    return geo_location_instance
