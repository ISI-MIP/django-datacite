import logging

from django.utils.dateparse import parse_date

from .models import Resource, Title, Description, Creator, Contributor, Subject, Date, \
                    AlternateIdentifier, RelatedIdentifier, Rights, \
                    Name, NameIdentifier, Identifier

logger = logging.getLogger(__name__)


def import_resource(data, resource_instance=None):
    if resource_instance is None:
        resource_instance = Resource()

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
            subject_instance, created = Subject.objects.update_or_create(
                resource=resource_instance,
                subject=subject_node.get('subject'),
                defaults={
                    'subject_scheme': subject_node.get('subjectScheme', ''),
                    'scheme_uri': subject_node.get('schemeURI', ''),
                    'value_uri': subject_node.get('valueURI', ''),
                    'classification_code': subject_node.get('classificationCode', '')
                }
            )
            logger.info('Subject="%s" %s', subject_instance, 'created' if created else 'updated')

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

                resource_type_general = related_identifier_node.get('resourceTypeGeneral')
                if RelatedIdentifier.validate_resource_type_general(resource_type_general):
                    resource_type_general = resource_type_general
                else:
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

    return resource_instance


def import_identifier(identifier_node):
    identifier = identifier_node.get('identifier')
    identifier_type = identifier_node.get('identifierType')

    if identifier and Identifier.validate_identifier_type(identifier_type):
        identifier_instance, created = Identifier.objects.update_or_create(
            identifier=identifier,
            identifier_type=identifier_type,
            defaults={
                'citation': identifier_node.get('citation', '')
            }
        )
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
    try:
        name_instance = Name.objects.get(name_identifiers__in=name_identifier_instances)
        logger.info('Name="%s" found by NameIdentifier', name_instance)
    except Name.DoesNotExist:
        name = name_node.get('name')
        if name is None:
            return

        try:
            name_instance = Name.objects.get(name=name)
            logger.info('Name="%s" found by Name', name_instance)
        except Name.DoesNotExist:
            name_type = name_node.get('nameType', Name.get_default_name_type())
            if not Name.validate_name_type(name_type):
                return

            name_instance = Name(name=name, name_type=name_type)
            logger.info('Name="%s" created', name_instance)

    # update the name instance
    name_instance.given_name = name_node.get('givenName', '')
    name_instance.family_name = name_node.get('familyName', '')
    name_instance.save()

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
