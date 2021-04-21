# -*- coding: utf-8 -*-
import json

import xbmcgui

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from ..mozie_request import Request
from .. import xbmc_helper as helper


def get_link(url, media):
    helper.log("Apply PLAYPHIM url %s - %s" % (media.get('originUrl'), url))
    # response = Request().get(url)
    parsed = urlparse(url)
    req_url = "https://proxy.playphim.info/proxy/proxy2.php?url={}".format(parse_qs(parsed.query)['id'][0])
    header = {
        'Referer': url
    }

    response = Request().get(req_url, headers=header)
    helper.log(response)
    sources = json.loads(response)
    helper.log(sources)
    listitems = []
    for source in sources:
        # print source.get('file')
        listitems.append("%s (%s)" % (source.get('label'), source.get('file')))

    index = xbmcgui.Dialog().select("Select stream", listitems)
    if index == -1:
        return None, None
    else:
        return sources[index].get('file') + "|%s" % urlencode(header), sources[index].get('label')

    return None, None
