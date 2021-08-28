# -*- coding: utf-8 -*-
from . import cors
try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from .. import xbmc_helper as helper
from .. import proxy_helper as proxy
from ..pastebin import PasteBin


def get_link(url, media):
    helper.log("Apply vanlongstreaming parser")
    base_url = urlparse(url)
    m_id = parse_qs(base_url.query).get('vid')[0]
    base_url = base_url.scheme + '://' + base_url.netloc

    url = '%s/hls/%s/playlist.m3u8' % (base_url, m_id)
    # header = {
    #     'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SAMSUNG SM-N960F Build/M1AJQ) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/8.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
    #     'Origin': base_url,
    #     'verifypeer': 'false'
    # }

    playlist = proxy.replace_proxy_link(url)
    url = PasteBin().dpaste(playlist, name='adaptivestream', expire=60)
    url = proxy.prepend_url(url, '-dl')
    return url, 'vanlong'

    return cors.get_link(url, media, True)
