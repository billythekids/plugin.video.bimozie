# -*- coding: utf-8 -*-

import json
from utils.mozie_request import Request
from urlparse import urlparse
import xbmcgui


def get_link(url, media):
    print "*********************** Apply fantvh url %s" % url
    request = Request()
    base_url = urlparse(url)
    path = urlparse(url).path.replace('/v/', '')
    base_url = base_url.scheme + '://' + base_url.netloc

    header = {
        'Referer': media.get('originUrl'),
        'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
        'Origin': base_url
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
