# -*- coding: utf-8 -*-
import re

import utils.xbmc_helper as helper
from utils.mozie_request import Request

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, media):
    print("*********************** Apply xemtivimienphi url %s" % url)
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        'referer': media.get('originUrl')
    }
    response = Request().get(url, headers=header)

    source = re.search(r'source:\s?"(.*?)",', response)
    if source:
        url = source.group(1)
    sources = re.search(r'sources:\s?(\[.*?\])', response)

    if sources:
        url = helper.convert_js_2_json(sources.group(1))[0]

    sources = re.search(r';link=(\[.*?\]);', response)

    if sources:
        url = helper.convert_js_2_json(sources.group(1))[0]

    source = re.search(r"video.src\s?=\s'(.*?)'", response)
    if source:
        url = source.group(1)

    base_url = urlparse(url)
    base_url = base_url.netloc

    header = {
        'origin': 'http://www.xemtivimienphi.com',
        'host': base_url,
        'verifypeer': 'false'
    }

    return url + "|%s" % urlencode(header), 'TVOnline'
