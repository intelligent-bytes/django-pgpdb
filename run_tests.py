#!/usr/bin/env python

import sys
import os

BASE_DIR = os.path.dirname(__file__)

import django
from django.conf import settings

def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests.
    try:
        settings.configure(
            TEMPLATES = [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': [
                        os.path.join(BASE_DIR, 'templates'),
                    ],
                    'APP_DIRS': True,
                },
            ],
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.admin',
                'django.contrib.sessions',
                'bootstrapform',
                'pgpdb',
            ],
            # Django replaces this, but it still wants it. *shrugs*
            DATABASE_ENGINE='django.db.backends.sqlite3',
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            TIME_ZONE = 'UTC',
            USE_I18N = True,
            USE_L10N = True,
            USE_TZ = True,
            MEDIA_ROOT='/tmp/django_pgpdb_test_media/',
            MEDIA_PATH='/media/',
            ROOT_URLCONF='pgpdb.urls',
            DEBUG=True,
            TEMPLATE_DEBUG=True,
        )

        if django.VERSION[:2] >= (1, 7):
            django.setup()

        apps = ['pgpdb']

        from django.core.management import call_command
        from django.test.utils import get_runner

        try:
            from django.contrib.auth import get_user_model
        except ImportError:
            USERNAME_FIELD = "username"
        else:
            USERNAME_FIELD = get_user_model().USERNAME_FIELD

        DjangoTestRunner = get_runner(settings)

        class TestRunner(DjangoTestRunner):
            def setup_databases(self, *args, **kwargs):
                result = super(TestRunner, self).setup_databases(*args, **kwargs)
                kwargs = {
                    "interactive": False,
                    "email": "admin@example.com",
                    USERNAME_FIELD: "admin",
                }
                call_command("createsuperuser", **kwargs)
                return result

        failures = TestRunner(verbosity=2, interactive=True).run_tests(apps)
        sys.exit(failures)
    finally:
        pass

if __name__ == '__main__':
    main()
