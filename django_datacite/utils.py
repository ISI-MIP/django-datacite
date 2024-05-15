import re

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


def render_citation(resource):
    citation = render_to_string('datacite/citation.html', context={'resource': resource})
    return ' '.join(citation.split())


def render_bibtex(resource):
    bibtex = render_to_string('datacite/resource.bib', {'resource': resource})
    # remove empty lines
    return '\n'.join([line for line in bibtex.splitlines() if line.strip()])


def update_version(string):
    seperator = get_settings('DATACITE_VERSION_SEPERATOR')
    pattern = get_settings('DATACITE_VERSION_PATTERN')

    re_pattern = re.compile(fr'[{seperator}]({pattern})$')

    match = re_pattern.search(string)
    if match:
        try:
            version = int(match.group(1)) + 1
        except ValueError:
            version = 1

        return re_pattern.sub(fr'{seperator}{version}', string)
    else:
        return f'{string}{seperator}1'
