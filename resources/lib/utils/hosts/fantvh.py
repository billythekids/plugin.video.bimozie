# -*- coding: utf-8 -*-

import json

from .. import xbmc_helper as helper
from ..mozie_request import Request

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs
import xbmcgui


def get_link(url, media):
    helper.log("*********************** Apply fantvh url %s" % url)
    request = Request()
    base_url = urlparse(url)
    path = urlparse(url).path.replace('/v/', '')
    base_url = base_url.scheme + '://' + base_url.netloc

    header = {
        'referer': media.get('originUrl'),
        'user-agent': "Chrome/59.0.3071.115 Safari/537.36",
        'origin': base_url
    }

    resp = request.post('https://fantvh.net/api/source/{}'.format(path), headers=header)
    resp = json.loads(resp)
    items = [(i['file'], i['label']) for i in resp['data']]
    items = sorted(items, key=lambda elem: int(elem[1][0:-1]), reverse=True)

    if len(items) == 1:
        return items[0][0], 'fantvh'

    listitems = []
    for i in items:
        listitems.append("%s (%s)" % (i[1], i[0]))
    index = xbmcgui.Dialog().select("Select fantvh stream", listitems)
    if index == -1:
        return None, None
    else:
        return items[index][0], 'fantvh'
