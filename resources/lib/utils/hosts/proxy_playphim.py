# -*- coding: utf-8 -*-
import re, json
import xbmcgui
from urlparse import urlparse, parse_qs
from urllib import urlencode
from utils.mozie_request import Request


def get_link(url, media):
    # response = Request().get(url)
    parsed = urlparse(url)
    req_url = "https://proxy.playphim.info/proxy/proxy2.php?url={}".format(parse_qs(parsed.query)['id'][0])
    header = {
        'Referer': url
    }

    response = Request().get(req_url, headers=header)
    sources = json.loads(response)
    listitems = []
    for source in sources:
        # print source.get('file')
        listitems.append("%s (%s)" % (source.get('label'), source.get('file')))

    index = xbmcgui.Dialog().select("Select stream", listitems)
    if index == -1:
        return None, None
    else:
        return sources[index].get('file') + "|%s" % urlencode(header),  sources[index].get('label')

    return None, None
