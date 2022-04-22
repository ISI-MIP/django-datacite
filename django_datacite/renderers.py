import io
from xml.dom.minidom import parseString
from xml.sax.saxutils import XMLGenerator


class XMLRenderer(object):

    def __init__(self):
        self.stream = io.StringIO()
        self.xml = XMLGenerator(self.stream, 'utf-8')

    def render(self, data):
        self.data = data
        self.render_document()

        dom = parseString(self.stream.getvalue())
        return dom.toprettyxml(indent='    ')

    def render_node(self, tag, attrs, value):
        if value is not None:
            # remove None values from attrs
            attrs = dict((k, v) for k, v in attrs.items() if v is not None)

            self.xml.startElement(tag, attrs)
            self.xml.characters(str(value))
            self.xml.endElement(tag)

    def render_document(self):
        self.xml.startDocument()
        self.render_resource()
        self.xml.endDocument()

    def render_resource(self):
        self.xml.startElement('resource', {
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xmlns': 'http://datacite.org/schema/kernel-4',
            'xsi:schemaLocation': 'http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.4/metadata.xsd'
        })

        # identifier
        identifiers = self.data.get('identifiers', [])
        if identifiers:
            self.render_node('identifier', {
                'identifierType': identifiers[0].get('identifierType')
            }, identifiers[0].get('identifier'))

        # creators
        creators = self.data.get('creators')
        if creators:
            self.xml.startElement('creators', {})
            for creator in creators:
                self.render_name('creator', creator)
            self.xml.endElement('creators')

        # titles
        titles = self.data.get('titles')
        if titles:
            self.xml.startElement('titles', {})
            for title in titles:
                self.render_node('title', {
                    'titleType': title.get('titleType')
                }, title.get('title'))
            self.xml.endElement('titles')

        # publisher
        self.render_node('publisher', {}, self.data.get('publisher'))

        # publicationYear
        self.render_node('publicationYear', {}, self.data.get('publicationYear'))

        # resourceType
        self.render_node('resourceType', {
            'resourceTypeGeneral': self.data.get('types', {}).get('resourceTypeGeneral', 'Dataset')
        }, self.data.get('types', {}).get('resourceType'))

        # subjects
        subjects = self.data.get('subjects')
        if subjects:
            self.xml.startElement('subjects', {})
            for subject in subjects:
                self.render_node('subject', {
                    'subjectScheme': subject.get('subjectScheme'),
                    'schemeURI': subject.get('schemeURI'),
                    'valueURI': subject.get('valueURI'),
                    'classificationCode': subject.get('classificationCode')
                }, subject.get('subject'))
            self.xml.endElement('subjects')

        # contributors
        contributors = self.data.get('contributors')
        if contributors:
            self.xml.startElement('contributors', {})
            for contributor in contributors:
                self.render_name('contributor', contributor)
            self.xml.endElement('contributors')

        # dates
        dates = self.data.get('dates')
        if dates:
            self.xml.startElement('dates', {})
            for date in dates:
                self.render_node('date', {
                    'dateType': date.get('dateType'),
                    'dateInformation': date.get('dateInformation')
                }, date.get('date'))
            self.xml.endElement('dates')

        # language
        self.render_node('language', {}, self.data.get('language'))

        # alternateIdentifiers
        alternate_identifiers = self.data.get('alternateIdentifiers')
        if alternate_identifiers:
            self.xml.startElement('alternateIdentifiers', {})
            for alternate_identifier in self.data.get('alternateIdentifiers', []):
                self.render_node('alternateIdentifier', {
                    'alternateIdentifierType': alternate_identifier.get('alternateIdentifierType')
                }, alternate_identifier.get('alternateIdentifier'))
            self.xml.endElement('alternateIdentifiers')

        # relatedIdentifiers
        related_identifiers = self.data.get('relatedIdentifiers')
        if related_identifiers:
            self.xml.startElement('relatedIdentifiers', {})
            for related_identifier in related_identifiers:
                if related_identifier.get('relatedIdentifier'):
                    self.render_node('relatedIdentifier', {
                        'relatedIdentifierType': related_identifier.get('relatedIdentifierType'),
                        'relationType': related_identifier.get('relationType'),
                        'resourceTypeGeneral': related_identifier.get('resourceTypeGeneral')
                    }, related_identifier.get('relatedIdentifier'))
            self.xml.endElement('relatedIdentifiers')

        # size
        self.render_node('size', {}, self.data.get('size'))

        # format
        self.render_node('format', {}, self.data.get('format'))

        # version
        self.render_node('version', {}, self.data.get('version'))

        # rightsList
        right_list = self.data.get('rightsList')
        if right_list:
            self.xml.startElement('rightsList', {})
            for rights in right_list:
                self.render_node('rights', {
                    'rightsURI': rights.get('rightsURI'),
                    'rightsIdentifier': rights.get('rightsIdentifier'),
                    'rightsIdentifierScheme': rights.get('rightsIdentifierScheme'),
                    'schemeURI': rights.get('schemeURI')
                }, rights.get('rights'))
            self.xml.endElement('rightsList')

        # descriptions
        descriptions = self.data.get('descriptions')
        if descriptions:
            self.xml.startElement('descriptions', {})
            for description in descriptions:
                self.render_node('description', {
                    'descriptionType': description.get('descriptionType', 'Abstract')
                }, description.get('description'))
            self.xml.endElement('descriptions')

        # geo location
        geo_locations = self.data.get('geoLocations')
        if geo_locations:
            self.xml.startElement('geoLocations', {})
            for geo_location in geo_locations:
                self.xml.startElement('geoLocation', {})

                geo_location_place = geo_location.get('geoLocationPlace')
                if geo_location_place:
                    self.render_node('geoLocationPlace', {}, geo_location_place)

                geo_location_point = geo_location.get('geoLocationPoint')
                if geo_location_point:
                    self.xml.startElement('geoLocationPoint', {})
                    self.render_node('pointLongitude', {}, geo_location_point.get('pointLongitude'))
                    self.render_node('pointLatitude', {}, geo_location_point.get('pointLatitude'))
                    self.xml.endElement('geoLocationPoint')

                geo_location_box = geo_location.get('geoLocationBox')
                if geo_location_box:
                    self.xml.startElement('geoLocationBox', {})
                    self.render_node('westBoundLongitude', {}, geo_location_box.get('westBoundLongitude'))
                    self.render_node('eastBoundLongitude', {}, geo_location_box.get('eastBoundLongitude'))
                    self.render_node('southBoundLatitude', {}, geo_location_box.get('southBoundLatitude'))
                    self.render_node('northBoundLatitude', {}, geo_location_box.get('northBoundLatitude'))
                    self.xml.endElement('geoLocationBox')

                geo_location_polygons = geo_location.get('geoLocationPolygons')
                if geo_location_polygons:
                    for geo_location_polygon in geo_location_polygons:
                        self.xml.startElement('geoLocationPolygon', {})
                        for polygon_point in geo_location_polygon.get('polygonPoints'):
                            self.xml.startElement('polygonPoint', {})
                            self.render_node('pointLongitude', {}, polygon_point.get('pointLongitude'))
                            self.render_node('pointLatitude', {}, polygon_point.get('pointLatitude'))
                            self.xml.endElement('polygonPoint')
                        in_point = geo_location_polygon.get('inPolygonPoint')
                        if in_point:
                            self.xml.startElement('inPolygonPoint', {})
                            self.render_node('pointLongitude', {}, in_point.get('pointLongitude'))
                            self.render_node('pointLatitude', {}, in_point.get('pointLatitude'))
                            self.xml.endElement('inPolygonPoint')
                        self.xml.endElement('geoLocationPolygon')

                self.xml.endElement('geoLocation')

            self.xml.endElement('geoLocations')

        # relatedIdentifiers
        funding_references = self.data.get('fundingReferences')
        if funding_references:
            self.xml.startElement('fundingReferences', {})
            for funding_reference in funding_references:
                self.xml.startElement('fundingReference', {})
                self.render_node('funderName', {}, funding_reference.get('funderName'))
                self.render_node('funderIdentifier', {
                    'funderIdentifierType': funding_reference.get('funderIdentifierType'),
                    'schemeURI': funding_reference.get('schemeURI'),
                }, funding_reference.get('funderIdentifier'))
                self.render_node('fundingReference', {}, funding_reference.get('fundingReference'))
                self.render_node('awardNumber', {}, funding_reference.get('awardNumber'))
                self.render_node('awardURI', {}, funding_reference.get('awardURI'))
                self.render_node('awardTitle', {}, funding_reference.get('awardTitle'))
                self.xml.endElement('fundingReference')
            self.xml.endElement('fundingReferences')

        self.xml.endElement('resource')

    def render_name(self, tag, name):
        contributor_type = name.get('contributorType')

        self.xml.startElement(tag, {'contributorType': contributor_type} if contributor_type else {})
        self.render_node(f'{tag}Name', {'nameType': name.get('nameType')}, name.get('name'))

        if name.get('givenName'):
            self.render_node('givenName', {}, name.get('givenName'))

        if name.get('familyName'):
            self.render_node('familyName', {}, name.get('familyName'))

        for name_identifier in name.get('nameIdentifiers', []):
            self.render_node('nameIdentifier', {
                'nameIdentifierScheme': name_identifier.get('nameIdentifierScheme'),
                'schemeURI': name_identifier.get('schemeURI')
            }, name_identifier.get('nameIdentifier'))

        for affiliation in name.get('affiliations', []):
            self.render_node('affiliation', {
                'affiliationIdentifier': affiliation.get('affiliationIdentifier'),
                'affiliationIdentifierScheme': affiliation.get('affiliationIdentifierScheme'),
                'schemeURI': affiliation.get('schemeURI')
            } if affiliation.get('affiliationIdentifier') else {}, affiliation.get('affiliation'))

        self.xml.endElement(tag)
