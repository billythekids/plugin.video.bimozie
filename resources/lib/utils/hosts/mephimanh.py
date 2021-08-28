# -*- coding: utf-8 -*-

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
from .. import xbmc_helper as helper
from ..mozie_request import Request

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, media):
    helper.log("*********************** Apply mephimanh url %s" % url)

    req = Request()
    req.head(url, redirect=False)
    url = req.get_request().headers['location']

    base_url = urlparse(media.get('originUrl'))
    base_url = base_url.scheme + '://' + base_url.netloc

    header = {
        'Referer': media.get('originUrl'),
        'Origin': base_url,
        'verifypeer': 'false'
    }

    return url + "|%s" % urlencode(header), "mephimanh"
