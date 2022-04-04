from django import forms
from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path

from .models import Resource, Title, Description, Creator, Contributor, Subject, Date, \
                    AlternateIdentifier, RelatedIdentifier, Rights, \
                    Name, NameIdentifier, Identifier
from .imports import import_resource


# Forms

class ResourceForm(forms.ModelForm):
    resource_type_general = forms.ChoiceField(
        initial=Resource.get_default_resource_type_general(),
        choices=Resource.get_resource_type_general_choices(),
        required=False
    )
    language = forms.ChoiceField(
        initial=Resource.get_default_language(),
        choices=Resource.get_language_choices(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial['publisher'] = Resource.get_default_publisher()


class TitleForm(forms.ModelForm):
    title_type = forms.ChoiceField(
        initial=Title.get_default_title_type(),
        choices=Title.get_title_type_choices(),
        required=False
    )


class DescriptionForm(forms.ModelForm):
    description_type = forms.ChoiceField(
        initial=Description.get_default_description_type(),
        choices=Description.get_description_type_choices()
    )


class ContributorForm(forms.ModelForm):
    contributor_type = forms.ChoiceField(
        initial=Contributor.get_default_contributor_type(),
        choices=Contributor.get_contributor_type_choices()
    )


class DateForm(forms.ModelForm):
    date_type = forms.ChoiceField(
        initial=Date.get_default_date_type(),
        choices=Date.get_date_type_choices()
    )


class RelatedIdentifierForm(forms.ModelForm):
    relation_type = forms.ChoiceField(
        initial=RelatedIdentifier.get_default_relation_type(),
        choices=RelatedIdentifier.get_relation_type_choices()
    )
    resource_type_general = forms.ChoiceField(
        initial=RelatedIdentifier.get_default_resource_type_general(),
        choices=RelatedIdentifier.get_resource_type_general_choices()
    )


class RightsForm(forms.ModelForm):

    rights_identifier = forms.ChoiceField(
        initial=Rights.get_default_rights_identifier(),
        choices=Rights.get_rights_identifier_choices()
    )

    def has_changed(self):
        # this always needs to be true since otherwise the only the default value
        # rights_identifier would not be saved
        return True


class NameForm(forms.ModelForm):
    name_type = forms.ChoiceField(
        initial=Name.get_default_name_type(),
        choices=Name.get_name_type_choices()
    )
    affiliations = forms.ModelMultipleChoiceField(
        queryset=Name.objects.filter(name_type=Name.get_affiliation_name_type()),
        required=False
    )


class NameIdentifierForm(forms.ModelForm):
    name_identifier_scheme = forms.ChoiceField(
        initial=NameIdentifier.get_default_name_identifier_scheme(),
        choices=NameIdentifier.get_name_identifier_scheme_choices()
    )


class IdentifierForm(forms.ModelForm):
    identifier_type = forms.ChoiceField(
        initial=Identifier.get_default_identifier_type(),
        choices=Identifier.get_identifier_type_choices()
    )


class ResourceUploadForm(forms.Form):
    file = forms.FileField()


# Inlines

class NoExtraInlineMixin(object):
    extra = 0


class TitleInline(NoExtraInlineMixin, admin.TabularInline):
    form = TitleForm
    model = Title


class DescriptionInline(NoExtraInlineMixin, admin.StackedInline):
    form = DescriptionForm
    model = Description


class CreatorInline(NoExtraInlineMixin, admin.TabularInline):
    model = Creator


class ContributorInline(NoExtraInlineMixin, admin.TabularInline):
    form = ContributorForm
    model = Contributor


class SubjectInline(NoExtraInlineMixin, admin.StackedInline):
    model = Subject


class DateInline(NoExtraInlineMixin, admin.TabularInline):
    form = DateForm
    model = Date


class AlternateIdentifierInline(NoExtraInlineMixin, admin.TabularInline):
    model = AlternateIdentifier


class RelatedIdentifierInline(NoExtraInlineMixin, admin.TabularInline):
    form = RelatedIdentifierForm
    model = RelatedIdentifier


class RightsInline(NoExtraInlineMixin, admin.TabularInline):
    form = RightsForm
    model = Rights


class NameIdentifierInline(NoExtraInlineMixin, admin.TabularInline):
    form = NameIdentifierForm
    model = NameIdentifier


# Admin

class ResourceAdmin(admin.ModelAdmin):
    form = ResourceForm
    inlines = (TitleInline, DescriptionInline, CreatorInline,
               ContributorInline, SubjectInline, DateInline,
               AlternateIdentifierInline, RelatedIdentifierInline,
               RightsInline)

    search_fields = ('identifier', )
    readonly_fields = ('citation', )
    list_display = ('identifier', 'title', 'resource_type_general', 'version')
    list_filter = ('resource_type_general', )

    def get_urls(self):
        return [
            path('import/', self.admin_site.admin_view(self.datecite_resource_import_create),
                 name='datecite_resource_import_create'),
            path('<int:pk>/import/', self.admin_site.admin_view(self.datecite_resource_import_update),
                 name='datecite_resource_import_update'),
            ] + super().get_urls()

    def datecite_resource_import_create(self, request):
        form = ResourceUploadForm(request.POST or None, request.FILES or None)

        if request.method == 'POST':
            if '_back' in request.POST:
                return redirect('admin:datacite_resource_list')

            elif '_send' in request.POST and form.is_valid():
                resource = import_resource(form.cleaned_data['file'])
                return redirect('admin:datacite_resource_change', object_id=resource.id)

        return render(request, 'admin/datacite/resource/import_form.html', context={
            'form': form
        })

    def datecite_resource_import_update(self, request, pk):
        resource = get_object_or_404(Resource, id=pk)
        form = ResourceUploadForm(request.POST or None, request.FILES or None)

        if request.method == 'POST':
            if '_back' in request.POST:
                return redirect('admin:datacite_resource_change', object_id=resource.id)

            elif '_send' in request.POST and form.is_valid():
                import_resource(form.cleaned_data['file'], resource)
                return redirect('admin:datacite_resource_change', object_id=resource.id)

        return render(request, 'admin/datacite/resource/import_form.html', context={
            'form': form
        })


class NameAdmin(admin.ModelAdmin):
    form = NameForm
    inlines = (NameIdentifierInline, )
    list_display = ('name', 'name_type')
    list_filter = ('name_type', )


class IdentifierAdmin(admin.ModelAdmin):
    form = IdentifierForm
    list_display = ('identifier', 'identifier_type')
    list_filter = ('identifier_type', )

    def get_readonly_fields(self, request, obj=None):
        if obj.resources_as_identifier.exists():
            return ['citation']
        else:
            return []


admin.site.register(Resource, ResourceAdmin)
admin.site.register(Name, NameAdmin)
admin.site.register(Identifier, IdentifierAdmin)
