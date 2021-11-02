# -*- coding: utf-8 -*-
import re
import time

from . import hls_parser as hls
from .. import proxy_helper as proxy
from ..link_extractor import LinkExtractor
from ..pastebin import PasteBin

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from ..mozie_request import Request
from .. import xbmc_helper as helper

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def get_link(url, media):
    helper.log("*********************** Apply donganime.net url %s" % url)
    req = Request()
    response = req.get(url)
    sources = LinkExtractor.play_sources(response)
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    if sources:
        url = '{}{}'.format(base_url, sources[0].get('file'))
        # return url, 'donganime'

    header = {
        'x-proxy-pass': str(round(time.time() * 1000))
    }

    content = hls.get_adaptive_link(req.get(url, headers=header))

    # https://stream3.donganime.net/files/247807c6cd80144fc5e267ad5de757ab_720p.mp4.m3u8
    # https://stream3.donganime.net/files/38d63efa61472cc4c3a5fbb963ca0094_720p.mp4.m3u8
    url = '{}{}'.format(base_url, content)
    content = req.get(url, headers=header)
    urls = re.findall(r'extinf.*\n(.*)', content, re.IGNORECASE)
    for link in urls:
        origin_link = link
        if link.startswith('//'):
            link = 'https:{}'.format(link)

        # proxy_url = '{}|{}'.format(link, urlencode(header))
        proxy_url = proxy.prepend_url(link, '-no')
        content = content.replace(origin_link, proxy_url)

    url = PasteBin().dpaste(content)

    return url, 'donganime'
    # return url + "|%s" % urlencode(header, safe=''), 'donganime'
