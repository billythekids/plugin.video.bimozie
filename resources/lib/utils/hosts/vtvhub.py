# -*- coding: utf-8 -*-
import re, json
from urlparse import urlparse
from urllib import urlencode
from . import cors, hls_parser
from utils.mozie_request import Request
from urlparse import urlparse, parse_qs


def get_link(url, movie):
    print "Apply VTVHUB parser"
    base_url = urlparse(url)

    is_ajax = re.search(r'embedplay', url)
    mid = parse_qs(base_url.query).get('id')[0]
    base_url = base_url.scheme + '://' + base_url.netloc

    if not mid:
        mid = re.search(r'\?id=((?:(?!\?).)*)', url) or re.search(r'embedplay/(.*)', url).group(1)

    if mid:
        header = {
            'Origin': base_url,
            'Referer': url
        }

        if not is_ajax:
            base_url = urlparse(url)
            base_url = base_url.scheme + '://' + base_url.netloc
            m_url = "%s/hls/%s/%s.playlist.m3u8" % (base_url, mid, mid)
            # m_url = hls_parser.get_stream(m_url, header, "%s/hls/%s" % (base_url, mid))
            # if 'http' not in url:
            #     url = base_url + url

        else:
            # https://dr.vtvhub.com/getLinkStreamMd5/411157b50473a98867d561aab273b4d2
            ajax_url = "%s/getLinkStreamMd5/%s" % (base_url, mid)
            response = json.loads(Request().get(ajax_url, headers=header))
            if len(response) > 0:
                m_url = response[0].get('file')

        return cors.get_link(m_url, movie, including_agent=False)

    return None, None

