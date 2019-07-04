"""Custom template tags"""

from django import template
# from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from django.conf import settings

register = template.Library()


@register.simple_tag
def full_url(request, url):
    """Generates full static file paths"""
    return host_url(request, static(url))


def host_url(request, uri):
    """Gets the host url"""

    if request:

        host = request.get_host()

        return '{0}://{1}{2}{3}'.format(
            'https' if settings.SSL_ENABLED else 'http', host,
            '' if uri.startswith('/') else '/', uri)
