# -*- coding: utf-8 -*-
import re, json
from urlparse import urlparse
from urllib import urlencode
from . import cors, hls_parser
from utils.mozie_request import Request


def get_link(url, movie):
    print "Apply VTVHUB parser"
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    is_ajax = re.search(r'embedplay', url)
    mid = re.search(r'\?id=((?:(?!\?).)*)', url) or re.search(r'embedplay/(.*)', url)

    if mid:
        header = {
            'Origin': base_url,
            'Referer': url
        }
        mid = mid.group(1)

        if not is_ajax:
            base_url = urlparse(url)
            base_url = base_url.scheme + '://' + base_url.netloc
            url = "%s/hls/%s/%s.playlist.m3u8" % (base_url, mid, mid)
            url = hls_parser.get_adaptive_link(Request().get(url, headers=header))
            if 'http' not in url:
                url = base_url + url

        else:
            # https://dr.vtvhub.com/getLinkStreamMd5/411157b50473a98867d561aab273b4d2
            ajax_url = "%s/getLinkStreamMd5/%s" % (base_url, mid)
            response = json.loads(Request().get(ajax_url , headers=header))
            if len(response) > 0:
                url = response[0].get('file')

    return cors.get_link(url, movie, including_agent=False)

