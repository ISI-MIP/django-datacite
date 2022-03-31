# Generated by Django 3.2.11 on 2022-03-31 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlternateIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('contributor_type', models.CharField(blank=True, max_length=32)),
            ],
            options={
                'ordering': ('order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=256)),
                ('identifier_type', models.CharField(max_length=32)),
                ('citation', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('name_type', models.CharField(max_length=32)),
                ('given_name', models.CharField(blank=True, max_length=256)),
                ('family_name', models.CharField(blank=True, max_length=256)),
                ('affiliations', models.ManyToManyField(blank=True, related_name='names_as_affiliations', to='datacite.Name')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('relation_type', models.CharField(max_length=32)),
                ('resource_type_general', models.CharField(blank=True, max_length=32)),
                ('identifier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacite.identifier')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publisher', models.CharField(blank=True, max_length=256)),
                ('publication_year', models.IntegerField(blank=True, null=True)),
                ('resource_type', models.CharField(blank=True, max_length=32)),
                ('resource_type_general', models.CharField(blank=True, max_length=32)),
                ('language', models.CharField(blank=True, max_length=32)),
                ('size', models.CharField(blank=True, max_length=32)),
                ('format', models.CharField(blank=True, max_length=32)),
                ('version', models.CharField(blank=True, max_length=32)),
                ('cite_publisher', models.BooleanField(default=True)),
                ('cite_resource_type_general', models.BooleanField(default=True)),
                ('cite_version', models.BooleanField(default=True)),
                ('alternate_identifiers', models.ManyToManyField(blank=True, related_name='resources_as_alternate_identifier', through='datacite.AlternateIdentifier', to='datacite.Identifier')),
                ('contributors', models.ManyToManyField(blank=True, related_name='resources_as_contributor', through='datacite.Contributor', to='datacite.Name')),
                ('creators', models.ManyToManyField(blank=True, related_name='resources_as_creator', through='datacite.Creator', to='datacite.Name')),
                ('identifier', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datacite.identifier')),
                ('related_identifiers', models.ManyToManyField(blank=True, related_name='resources_as_related_identifier', through='datacite.RelatedIdentifier', to='datacite.Identifier')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('title_type', models.CharField(blank=True, max_length=32)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='datacite.resource')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=256)),
                ('subject_scheme', models.CharField(blank=True, max_length=256)),
                ('scheme_uri', models.URLField(blank=True)),
                ('value_uri', models.URLField(blank=True)),
                ('classification_code', models.CharField(blank=True, max_length=32)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='datacite.resource')),
            ],
        ),
        migrations.CreateModel(
            name='Rights',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rights_identifier', models.CharField(max_length=128)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rights_list', to='datacite.resource')),
            ],
            options={
                'verbose_name_plural': 'Rights',
            },
        ),
        migrations.AddField(
            model_name='relatedidentifier',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacite.resource'),
        ),
        migrations.CreateModel(
            name='NameIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_identifier', models.CharField(max_length=256)),
                ('name_identifier_scheme', models.CharField(max_length=32)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name_identifiers', to='datacite.name')),
            ],
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('description_type', models.CharField(max_length=32)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descriptions', to='datacite.resource')),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('date_type', models.CharField(max_length=32)),
                ('date_information', models.CharField(blank=True, max_length=256)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dates', to='datacite.resource')),
            ],
        ),
        migrations.AddField(
            model_name='creator',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='datacite.name'),
        ),
        migrations.AddField(
            model_name='creator',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacite.resource'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacite.name'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacite.resource'),
        ),
        migrations.AddField(
            model_name='alternateidentifier',
            name='identifier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacite.identifier'),
        ),
        migrations.AddField(
            model_name='alternateidentifier',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacite.resource'),
        ),
    ]
