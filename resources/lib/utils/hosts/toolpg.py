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


def get_link(url, movie):
    base_url = urlparse(url)
    mid = parse_qs(base_url.query).get('id')[0]
    base_url = base_url.scheme + '://' + base_url.netloc

    try:
        hosturl = '%s/getLinkStreamMd5/%s' % (base_url, mid)
        header = {
            'Origin': base_url,
            'user-agent': "Chrome/59.0.3071.115 Safari/537.36",
            'Referer': url
        }

        items = json.loads(Request().get(hosturl, headers=header))
        if len(items)>0:
            listitems = []
            for i in items:
                listitems.append("%s (%s)" % (i['label'], i['file']))
            index = xbmcgui.Dialog().select("Select stream", listitems)
            if index == -1:
                return None, None
            else:
                return items[index]['file'], base_url
        else:
            return None, None
    except:
        pass

    # try:
    #     hosturl = '%s/hls/%s/%s.playlist.m3u8' % (base_url, mid, mid)
    #     header = {
    #         'Origin': base_url,
    #         'user-agent': "Chrome/59.0.3071.115 Safari/537.36",
    #         'Referer': url
    #     }
    #     return hosturl + "|%s" % urlencode(header), base_url
    # except:
    #     pass

    return url, base_url
