django-datacite
===============

[![Latest Release](https://img.shields.io/pypi/v/django-datacite)](https://pypi.org/project/django-datacite/)
[![Python Version](https://img.shields.io/badge/python->=3.8-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/ISI-MIP/django-datacite/blob/master/LICENSE)
[![pytest Workflow Status](https://github.com/ISI-MIP/django-datacite/actions/workflows/pytest.yml/badge.svg)](https://github.com/ISI-MIP/django-datacite/actions/workflows/pytest.yml)
[![Coverage Status](https://coveralls.io/repos/github/ISI-MIP/django-datacite/badge.svg?branch=master)](https://coveralls.io/github/ISI-MIP/django-datacite?branch=master)

A Django app to properly model the [DataCite Metadata Schema](https://schema.datacite.org/) in a relational database, with full integration into the Django admin interface. The app is *slightly* opinionated in a way to make it better usable as a DOI registration database. Names (`creators` and `contributors`) and identifiers (for the resources, but also for `alternativeIdentifiers` and `relatedIdentifiers`) are stored in separate database tables and can be reused for different resources. 

This app provides a set of [models](django_datacite/models.py), [admin classes](django_datacite/admin.py), [views](django_datacite/views.py), and utility functions to export and import DataCite files. All options and default settings can be customized in the Django `settings` using the same syntax as in [django_datacite/settings.py](django_datacite/settings.py). Identifiers have an additional `citation` field to store the human readable citation for reuse in other tools.

For a reference integration into a Django project see: https://github.com/ISI-MIP/isimip-doi.

**While it should already cover DataCite 4.3 completely, it is still under development should only be used with care.**
