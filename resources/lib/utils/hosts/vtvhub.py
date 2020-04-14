# -*- coding: utf-8 -*-
import re
from urlparse import urlparse
from urllib import urlencode
from . import cors, hls_parser
from utils.mozie_request import Request


def get_link(url, movie):
    print "Apply VTVHUB parser"
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    mid = re.search(r'\?id=((?:(?!\?).)*)', url)
    if mid:
        mid = mid.group(1)
        header = {
            'Origin': base_url,
            'Referer': url
        }

        base_url = urlparse(url)
        base_url = base_url.scheme + '://' + base_url.netloc
        url = "%s/hls/%s/%s.playlist.m3u8" % (base_url, mid, mid)
        url = hls_parser.get_adaptive_link(Request().get(url, headers=header))
        if 'http' not in url:
            url = base_url + url
    # else:
    return cors.get_link(url, movie, including_agent=False)

    # return url + "|%s" % urlencode(header), base_url
