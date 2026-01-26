django-datacite
===============

[![Latest release](https://img.shields.io/pypi/v/django-datacite.svg?style=flat)](https://pypi.python.org/pypi/django-datacite/)
[![License](https://img.shields.io/github/license/ISI-MIP/django-datacite?style=flat)](https://github.com/rdmorganiser/django-datacite/blob/main/LICENSE)
[![CI status](https://github.com/ISI-MIP/django-datacite/actions/workflows/ci.yml/badge.svg)](https://github.com/ISI-MIP/django-datacite/actions/workflows/ci.yml)
[![Coverage status](https://coveralls.io/repos/ISI-MIP/django-datacite/badge.svg?branch=main&service=github)](https://coveralls.io/github/ISI-MIP/django-datacite?branch=main)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18376443.svg)](https://doi.org/10.5281/zenodo.18376443)

A Django app to properly model the [DataCite Metadata Schema](https://schema.datacite.org/) in a relational database, with full integration into the Django admin interface. The app is *slightly* opinionated in a way to make it better usable as a DOI registration database. Names (`creators` and `contributors`) and identifiers (for the resources, but also for `alternativeIdentifiers` and `relatedIdentifiers`) are stored in separate database tables and can be reused for different resources.

This app provides a set of [models](django_datacite/models.py), [admin classes](django_datacite/admin.py), [views](django_datacite/views.py), and utility functions to export and import DataCite files. All options and default settings can be customized in the Django `settings` using the same syntax as in [django_datacite/settings.py](django_datacite/settings.py). Identifiers have an additional `citation` field to store the human readable citation for reuse in other tools.

For a reference integration into a Django project see: https://github.com/ISI-MIP/isimip-doi.

**Although it should cover DataCite 4.3 completely, it is still quite fresh and should be used with care.**
