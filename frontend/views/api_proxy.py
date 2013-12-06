# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.conf import settings
from urllib.parse import urlparse
import requests
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes


class IsProviderOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.organization.is_provider


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((TokenAuthentication, SessionAuthentication, ))
@permission_classes((IsAuthenticated, IsProviderOrReadOnly))
def proxy_view(request, path):
    """
    Adapted from https://github.com/mjumbewu/django-proxy

    Forward as close to an exact copy of the request as possible along to the
    given url.  Respond with as close to an exact copy of the resulting
    response as possible.
    """
    requests_args = get_requests_args(request, path)
    url = '/'.join([settings.EVENT_API_BASE_URL, path])

    response = requests.request(request.method, url, **requests_args)
    return process_response(response)


def get_requests_args(request, path):
    requests_args = {}

    if request.QUERY_PARAMS:
        requests_args['params'] = request.QUERY_PARAMS.dict()

    if request.body:
        requests_args['data'] = request.body

    headers = get_requests_headers(request, path)
    if headers:
        requests_args['headers'] = headers
    return requests_args


def get_requests_headers(request, path):
    """
    Retrieve the HTTP headers from a WSGI environment dictionary.
    """
    headers = {}
    for key, value in request.META.items():
        # Sometimes, things don't like when you send the requesting host
        # through.
        if key.startswith('HTTP_') and key != 'HTTP_HOST':
            headers[key[5:].replace('_', '-')] = value
        elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            headers[key.replace('_', '-')] = value

    headers.pop('AUTHORIZATION', None)
    headers.pop('COOKIE', None)
    # If there's a content-length header from Django, it's probably in all-caps
    # and requests might not notice it, so just remove it.
    for key in list(headers.keys()):
        if key.lower() == 'content-length':
            del headers[key]
    if request.user.organization.is_provider:
        headers['X-ODE-Provider-Id'] = request.user.pk
    headers['X-ODE-API-Mount-Point'] = get_api_mount_point(request, path)
    return headers


def get_api_mount_point(request, path):
    absolute_url = request.build_absolute_uri()
    path_length = len('/' + path)
    parsed_url = urlparse(absolute_url)
    if parsed_url.query:
        path_length += len('?' + parsed_url.query)
    return absolute_url[:-path_length]


def process_response(response):

    proxy_response = HttpResponse(response.content,
                                  status=response.status_code)

    excluded_headers = set([
        # Hop-by-hop headers
        # ------------------
        # Certain response headers should NOT be just tunneled through.  These
        # are they.  For more info, see:
        # http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.5.1
        'connection', 'keep-alive', 'proxy-authenticate',
        'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
        'upgrade',

        # Although content-encoding is not listed among the hop-by-hop headers,
        # it can cause trouble as well.  Just let the server set the value as
        # it should be.
        'content-encoding',

        # Since the remote server may or may not have sent the content in the
        # same encoding as Django will, let Django worry about what the length
        # should be.
        'content-length',
    ])
    for key, value in response.headers.items():
        if key.lower() in excluded_headers:
            continue
        proxy_response[key] = value
    return proxy_response
