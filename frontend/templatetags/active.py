from django import template
from django.core.urlresolvers import reverse_lazy

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, url):
    request = context['request']

    if url.startswith('/'):
        path = url
    else:
        path = reverse_lazy(url)

    if request.path == path:
        return 'active'

    return ''
