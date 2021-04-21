# -*- coding: utf-8 -*-
import json
import re

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs
from ..mozie_request import Request


def get_link(url):
    response = Request().get(url)
    sources = re.search(r'sources:\s(\[.*\]),', response)
    if sources:
        sources = json.loads(sources.group(1))
        url = sources[0]

    return url, 'vudeo'
