# -*- coding: utf-8 -*-
import re

from ..link_extractor import LinkExtractor
from ..mozie_request import Request
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
from . import cors
from .. import xbmc_helper as helper


def get_link(url, media):
    helper.log("*********************** Apply thuckhuya url %s" % url)
    req = Request()
    response = req.get(url)

    header = {
        'referer': 'https://thuckhuya.live/',
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
    }

    match = re.search(r'''<div id="player">(.*?)</div>''', response)
    if match:
        url = LinkExtractor.iframe(match.group(1))
        response = req.get(url, headers=header)

    match = re.search(r'''var urlStream = "(.*?)"''', response)
    if match:
        live_url = match.group(1)

    base_url = urlparse(url)
    base_url = '{}://{}/'.format(base_url.scheme, base_url.netloc)
    header = {
        'referer': base_url,
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
    }

    helper.log(req.get(live_url, headers=header))

    return live_url + "|%s" % urlencode(header), "thuckhuya"

    # return cors.get_link(url, media)
