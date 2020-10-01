# -*- coding: utf-8 -*-
import re, json
from urlparse import urlparse
from utils.mozie_request import Request


def get_link(url):
    response = Request().get(url)
    sources = re.search(r'sources:\s(\[.*\]),', response)
    if sources:
        sources = json.loads(sources.group(1))
        url = sources[0]

    return url, 'vudeo'
