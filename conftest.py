from pathlib import Path

import pytest

from django.conf import settings
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        fixtures = []
        for fixture_dir in settings.FIXTURE_DIRS:
            for file in Path(fixture_dir).iterdir():
                fixtures.append(file)

        call_command('loaddata', *fixtures)
