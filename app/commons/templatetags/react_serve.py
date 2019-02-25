from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static


register = template.Library()

# TODO Read these from env:

# Endpoint of the webpack server started by yarn/npm.
# Used when DEBUG = True in django.
REACT_ENDPOINT = settings.REACT_ENDPOINT
# JS folder in the static path where the webpack builds
# the final react script. Used when DEBUG = False in django.
REACT_BUILD_DIR = 'js'


@register.simple_tag
def react_serve(filename):
    if settings.DEBUG:
        return '{}/{}'.format(REACT_ENDPOINT, filename)
    return static('{}/{}'.format(REACT_BUILD_DIR, filename))
