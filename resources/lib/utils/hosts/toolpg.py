# -*- coding: utf-8 -*-
import re
from urlparse import urlparse, parse_qs
from urllib import urlencode


def get_link(url, movie):
    base_url = urlparse(url)
    mid = parse_qs(base_url.query).get('id')[0]
    base_url = base_url.scheme + '://' + base_url.netloc

    try:
        hosturl = '%s/hls/%s/%s.playlist.m3u8' % (base_url, mid, mid)
        header = {
            'Origin': base_url,
            'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
            'Referer': url
        }
        return hosturl + "|%s" % urlencode(header), base_url
    except:
        pass

    return url, base_url
