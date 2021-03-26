# -*- coding: utf-8 -*-
import re
try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs
from ..mozie_request import Request


def get_link(url):
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    try:
        response = Request().get(url)
        source = re.search(r'source[-\s]?=[-\s]?[\'|"](.*)[\'|"]', response)
        url = base_url + '/' + source.group(1)
    except:
        pass

    return url, 'vtv16'
