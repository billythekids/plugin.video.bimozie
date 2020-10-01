# -*- coding: utf-8 -*-
import re, json, base64
from urlparse import urlparse
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin
from urllib import urlencode
import hls_parser


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
            'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
            'Origin': base_url,
            'Referer': url
        }

        # return hls_parser.get_link(hosturl, movie)

        return hosturl + "|%s" % urlencode(header), 'manga123'

    except:
        pass

    return url, 'manga123.net'

