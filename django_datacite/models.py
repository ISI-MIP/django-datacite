from django.db import models
from django.utils.functional import cached_property

from .utils import get_settings, get_display_name, get_citation


class Resource(models.Model):

    identifier = models.ForeignKey(
        'Identifier', null=True, blank=True, on_delete=models.SET_NULL, related_name='resources_as_identifier'
    )
    publisher = models.CharField(
        max_length=256, blank=True
    )
    publication_year = models.IntegerField(
        blank=True, null=True,
    )
    resource_type = models.CharField(
        max_length=32, blank=True
    )
    resource_type_general = models.CharField(
        max_length=32, blank=True
    )
    language = models.CharField(
        max_length=32, blank=True
    )
    size = models.CharField(
        max_length=32, blank=True
    )
    format = models.CharField(
        max_length=32, blank=True
    )
    version = models.CharField(
        max_length=32, blank=True
    )
    cite_publisher = models.BooleanField(
        default=True
    )
    cite_resource_type_general = models.BooleanField(
        default=True
    )
    cite_version = models.BooleanField(
        default=True
    )
    creators = models.ManyToManyField(
        'Name', through='Creator', blank=True, related_name='resources_as_creator'
    )
    contributors = models.ManyToManyField(
        'Name', through='Contributor', blank=True, related_name='resources_as_contributor'
    )
    alternate_identifiers = models.ManyToManyField(
        'Identifier', through='AlternateIdentifier', blank=True, related_name='resources_as_alternate_identifier'
    )
    related_identifiers = models.ManyToManyField(
        'Identifier', through='RelatedIdentifier', blank=True, related_name='resources_as_related_identifier'
    )

    def __str__(self):
        return str(self.identifier)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.identifier:
            self.identifier.citation = self.citation
            self.identifier.save()

    def copy(self):
        # create and save new instance
        resource = Resource(
            identifier=self.identifier,
            publisher=self.publisher,
            publication_year=self.publication_year,
            resource_type=self.resource_type,
            resource_type_general=self.resource_type_general,
            language=self.language,
            size=self.size,
            format=self.format,
            version=self.version,
            cite_publisher=self.cite_publisher,
            cite_resource_type_general=self.cite_resource_type_general,
            cite_version=self.cite_version
        )
        resource.save()

        # copy related instances
        for title in self.titles.all():
            Title(
                resource=resource,
                title=title.title,
                title_type=title.title_type
            ).save()
        for description in self.descriptions.all():
            Description(
                resource=resource,
                description=description.description,
                description_type=description.description_type
            ).save()
        for creator in self.creator_set.all():
            Creator(
                resource=resource,
                name=creator.name,
                order=creator.order
            ).save()
        for contributor in self.contributor_set.all():
            Contributor(
                resource=resource,
                name=contributor.name,
                order=contributor.order,
                contributor_type=contributor.contributor_type
            ).save()
        for subject in self.subjects.all():
            Subject(
                resource=resource,
                subject=subject.subject,
                subject_scheme=subject.subject_scheme,
                scheme_uri=subject.scheme_uri,
                value_uri=subject.value_uri,
                classification_code=subject.classification_code
            ).save()
        for date in self.dates.all():
            Date(
                resource=resource,
                date=date.date,
                date_type=date.date_type
            ).save()
        for alternate_identifier in self.alternateidentifier_set.all():
            AlternateIdentifier(
                resource=resource,
                identifier=alternate_identifier.identifier,
                order=alternate_identifier.order
            ).save()
        for related_identifier in self.relatedidentifier_set.all():
            RelatedIdentifier(
                resource=resource,
                identifier=related_identifier.identifier,
                order=related_identifier.order,
                relation_type=related_identifier.relation_type,
                resource_type_general=related_identifier.resource_type_general
            ).save()
        for rights in self.rights_list.all():
            Rights(
                resource=resource,
                rights_identifier=rights.rights_identifier
            ).save()

        return resource

    @cached_property
    def title(self):
        main_title = self.titles.filter(title_type='').first()
        if main_title:
            return main_title.title

    @cached_property
    def citation(self):
        return get_citation(self)

    @staticmethod
    def get_default_publisher():
        return get_settings('DATACITE_DEFAULT_PUBLISHER')

    @staticmethod
    def get_default_resource_type_general():
        return get_settings('DATACITE_DEFAULT_RESOURCE_TYPE_GENERAL')

    @staticmethod
    def get_resource_type_general_choices():
        return get_settings('DATACITE_RESOURCE_TYPES_GENERAL')

    @classmethod
    def validate_resource_type_general(cls, resource_type):
        return resource_type in dict(cls.get_resource_type_general_choices())

    @staticmethod
    def get_default_language():
        return get_settings('DATACITE_DEFAULT_LANGUAGE')

    @staticmethod
    def get_language_choices():
        return get_settings('DATACITE_LANGUAGES')

    @classmethod
    def validate_language(cls, language):
        return language in dict(cls.get_language_choices())


class Identifier(models.Model):

    identifier = models.CharField(
        max_length=256
    )
    identifier_type = models.CharField(
        max_length=32
    )
    citation = models.TextField(
        blank=True
    )

    def __str__(self):
        return f'({self.identifier_type}) {self.identifier}'

    @staticmethod
    def get_default_identifier_type():
        return get_settings('DATACITE_DEFAULT_IDENTIFIER_TYPE')

    @staticmethod
    def get_identifier_type_choices():
        return get_settings('DATACITE_IDENTIFIER_TYPES')

    @classmethod
    def validate_identifier_type(cls, identifier_type):
        return identifier_type in dict(cls.get_identifier_type_choices())


class Name(models.Model):

    name = models.CharField(
        max_length=256
    )
    name_type = models.CharField(
        max_length=32
    )
    given_name = models.CharField(
        max_length=256, blank=True
    )
    family_name = models.CharField(
        max_length=256, blank=True
    )
    affiliations = models.ManyToManyField(
        'Name', blank=True, related_name='names_as_affiliations'
    )

    @staticmethod
    def get_default_name_type():
        return get_settings('DATACITE_DEFAULT_NAME_TYPE')

    @staticmethod
    def get_affiliation_name_type():
        return get_settings('DATACITE_AFFILIATION_NAME_TYPE')

    @staticmethod
    def get_name_type_choices():
        return get_settings('DATACITE_NAME_TYPES')

    @classmethod
    def validate_name_type(cls, name_type):
        return name_type in dict(cls.get_name_type_choices())

    def __str__(self):
        return self.name or f'{self.given_name} {self.family_name}'


class NameIdentifier(models.Model):

    name = models.ForeignKey(
        'Name', related_name='name_identifiers', on_delete=models.CASCADE,
    )
    name_identifier = models.CharField(
        max_length=256
    )
    name_identifier_scheme = models.CharField(
        max_length=32
    )

    def __str__(self):
        return f'({self.name_identifier_scheme}) {self.name_identifier}'

    @property
    def scheme_uri(self):
        return get_settings('DATACITE_IDENTIFIER_SCHEME_URIS', {}).get(self.name_identifier_scheme)

    @staticmethod
    def get_default_name_identifier_scheme():
        return get_settings('DATACITE_DEFAULT_NAME_IDENTIFIER_SCHEME')

    @staticmethod
    def get_name_identifier_scheme_choices():
        return get_settings('DATACITE_NAME_IDENTIFIER_SCHEMES')

    @classmethod
    def validate_name_identifier_scheme(cls, name_identifier_scheme):
        return name_identifier_scheme in dict(cls.get_name_identifier_scheme_choices())


class Creator(models.Model):

    resource = models.ForeignKey(
        'Resource', on_delete=models.CASCADE
    )
    name = models.ForeignKey(
        'Name', related_name='creator', on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ('order', 'name')

    def __str__(self):
        return f'{self.name}'


class Contributor(models.Model):

    resource = models.ForeignKey(
        'Resource', on_delete=models.CASCADE
    )
    name = models.ForeignKey(
        'Name', on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(
        default=0
    )
    contributor_type = models.CharField(
        max_length=32, blank=True
    )

    class Meta:
        ordering = ('order', 'name')

    def __str__(self):
        return f'{self.contributor_type}: {self.name}'

    @staticmethod
    def get_default_contributor_type():
        return get_settings('DATACITE_DEFAULT_CONTRIBUTOR_TYPE')

    @staticmethod
    def get_contributor_type_choices():
        return get_settings('DATACITE_CONTRIBUTOR_TYPES')

    @classmethod
    def validate_contributor_type(cls, contributor_type):
        return contributor_type in dict(cls.get_contributor_type_choices())


class Title(models.Model):

    resource = models.ForeignKey(
        'Resource', related_name='titles', on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=256
    )
    title_type = models.CharField(
        max_length=32, blank=True
    )

    def __str__(self):
        if self.title_type:
            return f'{self.title_type}: {self.title}'
        else:
            return self.title

    @staticmethod
    def get_default_title_type():
        return get_settings('DATACITE_DEFAULT_TITLE_TYPE')

    @staticmethod
    def get_title_type_choices():
        return get_settings('DATACITE_TITLE_TYPES')

    @classmethod
    def validate_title_type(cls, title_type):
        return title_type in dict(cls.get_title_type_choices())


class Description(models.Model):

    resource = models.ForeignKey(
        'Resource', related_name='descriptions', on_delete=models.CASCADE
    )
    description = models.TextField()
    description_type = models.CharField(
        max_length=32
    )

    def __str__(self):
        return f'{self.description_type} : {self.resource}'

    @cached_property
    def escaped_description(self):
        return self.description.replace('\r\n', '\n').replace('\n\n', '<br>').replace('\n', ' ')

    @staticmethod
    def get_default_description_type():
        return get_settings('DATACITE_DEFAULT_DESCRIPTION_TYPE')

    @staticmethod
    def get_description_type_choices():
        return get_settings('DATACITE_DESCRIPTION_TYPES')

    @classmethod
    def validate_description_type(cls, description_type):
        return description_type in dict(cls.get_description_type_choices())


class Subject(models.Model):

    resource = models.ForeignKey(
        'Resource', related_name='subjects', on_delete=models.CASCADE,
    )
    subject = models.CharField(
        max_length=256
    )
    subject_scheme = models.CharField(
        max_length=256, blank=True
    )
    scheme_uri = models.URLField(
        blank=True
    )
    value_uri = models.URLField(
        blank=True
    )
    classification_code = models.CharField(
        max_length=32, blank=True
    )

    def __str__(self):
        return self.subject


class Date(models.Model):

    resource = models.ForeignKey(
        'Resource', related_name='dates', on_delete=models.CASCADE,
    )
    date = models.DateField()
    date_type = models.CharField(
        max_length=32
    )
    date_information = models.CharField(
        max_length=256, blank=True
    )

    def __str__(self):
        return f'{self.date_type}: {self.date}'

    @staticmethod
    def get_default_date_type():
        return get_settings('DATACITE_DEFAULT_DATE_TYPE')

    @staticmethod
    def get_date_type_choices():
        return get_settings('DATACITE_DATE_TYPES')

    @classmethod
    def validate_date_type(cls, date_type):
        return date_type in dict(cls.get_date_type_choices())


class AlternateIdentifier(models.Model):

    resource = models.ForeignKey(
        'Resource', on_delete=models.CASCADE
    )
    identifier = models.ForeignKey(
        'Identifier', on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return str(self.identifier)


class RelatedIdentifier(models.Model):

    resource = models.ForeignKey(
        'Resource', on_delete=models.CASCADE
    )
    identifier = models.ForeignKey(
        'Identifier', on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(
        default=0
    )
    relation_type = models.CharField(
        max_length=32
    )
    resource_type_general = models.CharField(
        max_length=32, blank=True
    )

    def __str__(self):
        return str(self.identifier)

    @staticmethod
    def get_default_relation_type():
        return get_settings('DATACITE_DEFAULT_RELATION_TYPE')

    @staticmethod
    def get_relation_type_choices():
        return get_settings('DATACITE_RELATION_TYPES')

    @classmethod
    def validate_relation_type(cls, relation_type):
        return relation_type in dict(cls.get_relation_type_choices())

    @staticmethod
    def get_default_resource_type_general():
        return get_settings('DATACITE_DEFAULT_RESOURCE_TYPE_GENERAL')

    @staticmethod
    def get_resource_type_general_choices():
        return get_settings('DATACITE_RESOURCE_TYPES_GENERAL')

    @classmethod
    def validate_resource_type_general(cls, resource_type_general):
        return resource_type_general in dict(cls.get_resource_type_general_choices())


class Rights(models.Model):

    resource = models.ForeignKey(
        'Resource', related_name='rights_list', on_delete=models.CASCADE
    )
    rights_identifier = models.CharField(
        max_length=128
    )

    class Meta:
        verbose_name_plural = 'Rights'

    def __str__(self):
        return self.rights_identifier

    @property
    def rights(self):
        return get_display_name(self.rights_identifier, self.get_rights_identifier_choices())

    @property
    def rights_uri(self):
        return get_settings('DATACITE_RIGHTS_IDENTIFIER_URIS', {}).get(self.rights_identifier)

    @property
    def rights_identifier_scheme(self):
        return get_settings('DATACITE_RIGHTS_IDENTIFIER_SCHEMES', {}).get(self.rights_identifier)

    @property
    def scheme_uri(self):
        return get_settings('DATACITE_RIGHTS_IDENTIFIER_SCHEME_URIS', {}).get(self.rights_identifier_scheme)

    @staticmethod
    def get_default_rights_identifier():
        return get_settings('DATACITE_DEFAULT_RIGHTS_IDENTIFIER')

    @staticmethod
    def get_rights_identifier_choices():
        return get_settings('DATACITE_RIGHTS_IDENTIFIERS')

    @classmethod
    def validate_rights_identifier(cls, rights_identifier):
        return rights_identifier in dict(cls.get_rights_identifier_choices())

    @staticmethod
    def get_rights_identifier_by_uri(uri):
        # get the uri map, reverse it row by row with map, creates a dict again, and look for the uri with get
        return dict(map(reversed, get_settings('DATACITE_RIGHTS_IDENTIFIER_URIS', {}).items())).get(uri)
