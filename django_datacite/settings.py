from django.utils.translation import gettext as _

DOI_BASE_URL = 'https://doi.org/'

DATACITE_VERSION_SEPERATOR = '.'
DATACITE_VERSION_PATTERN = r'\d{1,3}'
DATACITE_PREVIOUS_VERSION_ORDER = 1000
DATACITE_NEW_VERSION_ORDER = 2000

DATACITE_DEFAULT_IDENTIFIER_TYPE = 'DOI'
DATACITE_IDENTIFIER_TYPES = (
    ('ARK', _('ARK')),
    ('arXiv', _('arXiv')),
    ('bibcode', _('bibcode')),
    ('DOI', _('DOI')),
    ('EAN13', _('EAN13')),
    ('EISSN', _('EISSN')),
    ('Handle', _('Handle')),
    ('IGSN', _('IGSN')),
    ('ISBN', _('ISBN')),
    ('ISSN', _('ISSN')),
    ('ISTC', _('ISTC')),
    ('LISSN', _('LISSN')),
    ('LSID', _('LSID')),
    ('PMID', _('PMID')),
    ('PURL', _('PURL')),
    ('UPC', _('UPC')),
    ('URL', _('URL')),
    ('URN', _('URN')),
    ('w3id', _('w3id')),
)

DATACITE_IDENTIFIER_SCHEME_URIS = {
    'ISNI': 'https://isni.org',
    'ORCID': 'https://orcid.org',
    'ROR': 'https://ror.org',
    'GRID': 'https://www.grid.ac'
}

DATACITE_DEFAULT_RESOURCE_TYPE_GENERAL = 'Dataset'
DATACITE_RESOURCE_TYPES_GENERAL = (
    ('Audiovisual', _('Audiovisual')),
    ('Book', _('Book')),
    ('BookChapter', _('BookChapter')),
    ('Collection', _('Collection')),
    ('ComputationalNotebook', _('ComputationalNotebook')),
    ('ConferencePaper', _('ConferencePaper')),
    ('ConferenceProceeding', _('ConferenceProceeding')),
    ('DataPaper', _('DataPaper')),
    ('Dataset', _('Dataset')),
    ('Dissertation', _('Dissertation')),
    ('Event', _('Event')),
    ('Image', _('Image')),
    ('InteractiveResource', _('InteractiveResource')),
    ('Journal', _('Journal')),
    ('JournalArticle', _('JournalArticle')),
    ('Model', _('Model')),
    ('OutputManagementPlan', _('OutputManagementPlan')),
    ('PeerReview', _('PeerReview')),
    ('PhysicalObject', _('PhysicalObject')),
    ('Preprint', _('Preprint')),
    ('Report', _('Report')),
    ('Service', _('Service')),
    ('Software', _('Software')),
    ('Sound', _('Sound')),
    ('Standard', _('Standard')),
    ('Text', _('Text')),
    ('Workflow', _('Workflow')),
    ('Other', _('Other')),
)

DATACITE_DEFAULT_LANGUAGE = 'en'
DATACITE_LANGUAGES = (
    ('en', _('English')),
)

DATACITE_DEFAULT_TITLE_TYPE = ''
DATACITE_TITLE_TYPES = (
    ('', _('Main title')),
    ('AlternativeTitle', _('Alternative title')),
    ('Subtitle', _('Subtitle')),
    ('TranslatedTitle', _('Translated title')),
    ('Other', _('Other')),
)

DATACITE_DEFAULT_NAME_TYPE = 'Personal'
DATACITE_AFFILIATION_NAME_TYPE = 'Organizational'
DATACITE_NAME_TYPES = (
    ('Personal', _('Personal')),
    ('Organizational', _('Organizational'))
)

DATACITE_DEFAULT_DESCRIPTION_TYPE = 'Abstract'
DATACITE_DESCRIPTION_TYPES = (
    ('Abstract', _('Abstract')),
    ('Methods', _('Methods')),
    ('SeriesInformation', _('SeriesInformation')),
    ('TableOfContents', _('TableOfContents')),
    ('TechnicalInfo', _('TechnicalInfo')),
    ('Other', _('Other')),
)

DATACITE_DEFAULT_NAME_IDENTIFIER_SCHEME = 'ORCID'
DATACITE_NAME_IDENTIFIER_SCHEMES = (
    ('ORCID', _('ORCID')),
    ('ISNI', _('ISNI')),
    ('ROR', _('ROR')),
    ('GRID', _('GRID')),
)

DATACITE_DEFAULT_CONTRIBUTOR_TYPE = 'ContactPerson'
DATACITE_CONTRIBUTOR_TYPES = (
    ('ContactPerson', _('ContactPerson')),
    ('DataCollector', _('DataCollector')),
    ('DataCurator', _('DataCurator')),
    ('DataManager', _('DataManager')),
    ('Distributor', _('Distributor')),
    ('Editor', _('Editor')),
    ('HostingInstitution', _('HostingInstitution')),
    ('Producer', _('Producer')),
    ('ProjectLeader', _('ProjectLeader')),
    ('ProjectManager', _('ProjectManager')),
    ('ProjectMember', _('ProjectMember')),
    ('RegistrationAgency', _('RegistrationAgency')),
    ('RegistrationAuthority', _('RegistrationAuthority')),
    ('RelatedPerson', _('RelatedPerson')),
    ('Researcher', _('Researcher')),
    ('ResearchGroup', _('ResearchGroup')),
    ('RightsHolder', _('RightsHolder')),
    ('Sponsor', _('Sponsor')),
    ('Supervisor', _('Supervisor')),
    ('WorkPackageLeader', _('WorkPackageLeader')),
    ('Other', _('Other')),
)

DATACITE_DEFAULT_DATE_TYPE = 'Issued'
DATACITE_DATE_TYPES = (
    ('Accepted', _('Accepted')),
    ('Available', _('Available')),
    ('Copyrighted', _('Copyrighted')),
    ('Collected', _('Collected')),
    ('Created', _('Created')),
    ('Issued', _('Issued')),
    ('Submitted', _('Submitted')),
    ('Updated', _('Updated')),
    ('Valid', _('Valid')),
    ('Withdrawn', _('Withdrawn')),
    ('Other', _('Other')),
)

DATACITE_DEFAULT_RELATION_TYPE = 'References'
DATACITE_RELATION_TYPES = (
    ('IsCitedBy', _('IsCitedBy')),
    ('Cites', _('Cites')),
    ('IsSupplementTo', _('IsSupplementTo')),
    ('IsSupplementedBy', _('IsSupplementedBy')),
    ('IsContinuedBy', _('IsContinuedBy')),
    ('Continues', _('Continues')),
    ('IsDescribedBy', _('IsDescribedBy')),
    ('Describes', _('Describes')),
    ('HasMetadata', _('HasMetadata')),
    ('IsMetadataFor', _('IsMetadataFor')),
    ('HasVersion', _('HasVersion')),
    ('IsVersionOf', _('IsVersionOf')),
    ('IsNewVersionOf', _('IsNewVersionOf')),
    ('IsPreviousVersionOf', _('IsPreviousVersionOf')),
    ('IsPartOf', _('IsPartOf')),
    ('HasPart', _('HasPart')),
    ('IsPublishedIn', _('IsPublishedIn')),
    ('IsReferencedBy', _('IsReferencedBy')),
    ('References', _('References')),
    ('IsDocumentedBy', _('IsDocumentedBy')),
    ('Documents', _('Documents')),
    ('IsCompiledBy', _('IsCompiledBy')),
    ('Compiles', _('Compiles')),
    ('IsVariantFormOf', _('IsVariantFormOf')),
    ('IsOriginalFormOf', _('IsOriginalFormOf')),
    ('IsIdenticalTo', _('IsIdenticalTo')),
    ('IsReviewedBy', _('IsReviewedBy')),
    ('Reviews', _('Reviews')),
    ('IsDerivedFrom', _('IsDerivedFrom')),
    ('IsSourceOf', _('IsSourceOf')),
    ('IsRequiredBy', _('IsRequiredBy')),
    ('Requires', _('Requires')),
    ('IsObsoletedBy', _('IsObsoletedBy')),
    ('Obsoletes', _('Obsoletes')),
)

DATACITE_DEFAULT_RIGHTS_IDENTIFIER = 'CC0-1.0'
DATACITE_RIGHTS_IDENTIFIERS = (
    ('CC0-1.0',
        _('CC0 1.0 Universal Public Domain Dedication')),
    ('CC-BY-4.0',
        _('Creative Commons Attribution 4.0 International (CC BY 4.0)')),
    ('CC-BY-SA-4.0',
        _('Creative Commons Attribution Share Alike 4.0 International (CC BY-SA 4.0)')),
    ('CC-BY-NC-4.0',
        _('Creative Commons Attribution Non Commercial 4.0 International (CC BY-NC 4.0)')),
    ('CC-BY-NC-SA-4.0',
        _('Creative Commons Attribution Non Commercial Share Alike 4.0 International (CC BY-NC-SA 4.0)')),
)

DATACITE_RIGHTS_IDENTIFIER_URIS = {
    'CC0-1.0': 'https://creativecommons.org/publicdomain/zero/1.0/',
    'CC-BY-4.0': 'https://creativecommons.org/licenses/by/4.0/',
    'CC-BY-SA-4.0': 'https://creativecommons.org/licenses/by-sa/4.0/',
    'CC-BY-NC-4.0': 'https://creativecommons.org/licenses/by-nc/4.0/',
    'CC-BY-NC-SA-4.0': 'https://creativecommons.org/licenses/by-nc-sa/4.0/'
}

DATACITE_RIGHTS_IDENTIFIER_SCHEMES = {
    'CC0-1.0': 'SPDX',
    'CC-BY-4.0': 'SPDX',
    'CC-BY-SA-4.0': 'SPDX',
    'CC-BY-NC-4.0': 'SPDX',
    'CC-BY-NC-SA-4.0': 'SPDX'
}

DATACITE_RIGHTS_IDENTIFIER_SCHEME_URIS = {
    'SPDX': 'https://spdx.org/licenses/'
}

DATACITE_DEFAULT_NUMBER_TYPE = 'Article'
DATACITE_NUMBER_TYPES = (
    ('Article', 'Article'),
    ('Chapter', 'Chapter'),
    ('Report', 'Report'),
    ('Other', 'Other')
)

DATACITE_DEFAULT_SUBJECT_SCHEME = ''
DATACITE_DEFAULT_SUBJECT_SCHEME_URI = ''
