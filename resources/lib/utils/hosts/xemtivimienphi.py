# -*- coding: utf-8 -*-
import re

from .. import xbmc_helper as helper
from ..mozie_request import Request

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, media):
    helper.log("*********************** Apply xemtivimienphi url %s" % url)
    header = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        'referer': media.get('originUrl')
    }

    req = Request()

    response = req.get(url, headers=header)
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
        # 'origin': 'http://www.xemtivimienphi.com',
        # 'x-forwarded-host': base_url,
        # 'referer': base_url,
        # 'verifypeer': 'false',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
    }

    helper.log(req.get(url, headers=header))
    return url + "|%s" % urlencode(header), 'TVOnline'
