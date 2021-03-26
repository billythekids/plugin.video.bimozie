# -*- coding: utf-8 -*-

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs
from . import cors
from ..mozie_request import Request


def get_link(url, media, include_header=True):
    base_url = urlparse(media.get('originUrl'))
    base_url = base_url.scheme + '://' + base_url.netloc
    host_url = urlparse(url)

    r = Request()
    r.head(url)
    if include_header:
        return cors.get_link(r.get_request().history[0].headers['Location'], media)

    return r.get_request().history[0].headers['Location'], host_url.netloc
