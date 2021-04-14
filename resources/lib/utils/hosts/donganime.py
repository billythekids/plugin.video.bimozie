# -*- coding: utf-8 -*-
import time

from ..link_extractor import LinkExtractor
from ..pastebin import PasteBin

from . import hls_parser as hls

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
    if sources:
        base_url = urlparse(url)
        base_url = base_url.scheme + '://' + base_url.netloc
        url = '{}{}'.format(base_url, sources[0].get('file'))
        print(url)
        return url, 'donganime'

    content = hls.get_adaptive_link(req.get(url))

    # https://stream3.donganime.net/files/247807c6cd80144fc5e267ad5de757ab_720p.mp4.m3u8
    # https://stream3.donganime.net/files/38d63efa61472cc4c3a5fbb963ca0094_720p.mp4.m3u8
    url = 'https://stream3.donganime.net{}'.format(content)
    header = {
        'x-proxy-pass': str(round(time.time()*1000))
    }

    url = PasteBin().dpaste(req.get(url, headers=header))

    return url, 'donganime'
    # return url + "|%s" % urlencode(header, safe=''), 'donganime'
