# -*- coding: utf-8 -*-
import json
import re

import xbmcgui
from ..mozie_request import Request

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from .. import xbmc_helper as helper


def get_link(url, media):
    request = Request()
    base_url = urlparse(media.get('originUrl'))
    base_url = base_url.scheme + '://' + base_url.netloc
    header = {
        'Referer': url,
        'user-agent': "Chrome/59.0.3071.115 Safari/537.36",
        'Origin': base_url
    }

    helper.log("Apply iframeembed url %s" % url)

    resp = request.get(url, headers=header)
    req = request.get_request()
    if req.history:
        r_url = req.url
        rurl = urlparse(r_url)
        rurl = rurl.scheme + '://' + rurl.netloc
        rid = re.search(r'id=(.*)', r_url).group(1)
        rurl = "{}/getLinkStreamMd5/{}".format(rurl, rid)
        sources = request.get(rurl, headers=header)
        sources = json.loads(sources)
    else:
        sources = re.search(r'sources\s?[=:]\s?(\[.*?\])', resp, re.DOTALL)
        if sources:
            sources = "".join([s for s in sources.group(1).splitlines() if s.strip("\r\n")])
            sources = re.sub(r'\s+', '', sources)
            sources = helper.convert_js_2_json(sources)

    if sources:
        if len(sources) > 1:
            listitems = []
            for i in sources:
                listitems.append("%s (%s)" % (i.get('label'), i.get('file')))
            index = xbmcgui.Dialog().select("Select stream", listitems)
            if index == -1:
                return None, None
            else:
                return sources[index].get('file') + "|%s" % urlencode(header), sources[index].get('label')
        else:
            return sources[0].get('file') + "|%s" % urlencode(header), sources[0].get('label')

    return None, None
