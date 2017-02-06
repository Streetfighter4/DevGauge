import os

from raven.contrib.django.management.commands import raven

class MyConfig(object):
    SENTRY_CONFIG = {
        'dsn': 'https://<key>:<secret>@sentry.io/<project>',
        'include_paths': ['myproject'],
        'release': raven.fetch_git_sha(os.path.dirname(__file__)),
    }