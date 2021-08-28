# -*- coding: utf-8 -*-
import re

from .. import proxy_helper as proxy
from ..pastebin import PasteBin

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, movie):
    #     https://loadbalance.manga123.net/hls/08bb5dbe0b1b06c71d5d960d280d2c81/08bb5dbe0b1b06c71d5d960d280d2c81.m3u8
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    try:
        mid = re.search(r'\?id=(.*)&sub', url) or re.search(r'\?id=(.*)', url)
        mid = mid.group(1)
        # hosturl = '%s/hls/%s/%s.m3u8' % (base_url, mid, mid)
        hosturl = '%s/playlist/%s/1601558354231' % (base_url, mid)

        header = {
            'user-agent': "Chrome/59.0.3071.115 Safari/537.36",
            'Origin': base_url,
            'Referer': url
        }

        adaptive_link = proxy.get_adaptive_link(hosturl)
        playlist = proxy.replace_proxy_link(adaptive_link, headers=header)
        return PasteBin().dpaste(playlist, name='adaptivestream', expire=60), 'manga123'
    except:
        pass

    return url, 'manga123.net'
