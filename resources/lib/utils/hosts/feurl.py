# -*- coding: utf-8 -*-
import json
import re

from .. import xbmc_helper as helper
import xbmcgui

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
from ..mozie_request import Request

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, media):
    helper.log("*********************** Apply furl url %s" % url)
    request = Request()

    base_url = urlparse(media.get('originUrl'))
    base_url = base_url.scheme + '://' + base_url.netloc
    header = {
        # 'Referer': media.get('originUrl'),
        # 'user-agent': "Chrome/59.0.3071.115 Safari/537.36",
        'Referer': url
    }

    mid = re.search('/v/(.*)', url).group(1)
    response = Request().post('https://feurl.com/api/source/%s' % mid, params={
        'd': 'feurl.com', 'r': ''
    })
    response = json.loads(response)
    sources = response['data']

    if sources:
        if len(sources) > 1:
            listitems = []
            for i in sources:
                listitems.append("%s (%s)" % (i.get('label'), i.get('file')))
            index = xbmcgui.Dialog().select("Select stream", listitems)
            if index == -1:
                return None, None
            else:
                return get_stream(sources[index].get('file'), header), sources[index].get('label')
        else:
            return get_stream(sources[0].get('file'), header), sources[0].get('label')

    return None, None


def get_stream(url, header):
    if 'fvs.io' in url:
        request = Request()
        request.head(url, headers=header)
        req = request.get_request()
        if req.history:
            return req.url + "|%s" % urlencode(header)
    return url
