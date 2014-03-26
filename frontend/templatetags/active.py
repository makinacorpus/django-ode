
import logging

from django import template
from django.core.urlresolvers import reverse_lazy, NoReverseMatch

register = template.Library()


logger = logging.getLogger('frontend')


@register.simple_tag(takes_context=True)
def active(context, url):

    try:
        request = context['request']

        if url.startswith('/'):
            path = url
        else:
            path = reverse_lazy(url)

        if request.path == path:
            return 'active'
    except NoReverseMatch as e:
        logger.error(str(e))

    return ''
