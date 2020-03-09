# -*- coding: utf-8 -*-
import re
import json
from urlparse import urlparse, parse_qs
from urllib import urlencode


def get_link(url, media):
    base_url = urlparse(url)
    id = parse_qs(base_url.query).get('id')[0]
    base_url = base_url.scheme + '://' + base_url.netloc

    header = {
        'Referer': url,
        # 'Origin': base_url,
        # 'User-Agent': "Chrome/59.0.3071.115 Safari/537.36"
    }

    return '%s/hls/%s/%s.playlist.m3u8|%s' % (base_url, id, id, urlencode(header)), 'vanlong'
