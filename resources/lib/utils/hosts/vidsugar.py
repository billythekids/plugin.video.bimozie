# -*- coding: utf-8 -*-
import re

from six.moves.urllib.parse import unquote

from .. import proxy_helper as proxy
from ..pastebin import PasteBin

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, media, noneTruncate=False):
    headers = {
        'referer': media.get('originUrl')
    }

    if not noneTruncate:
        adaptive_link = proxy.get_adaptive_link(url, headers=headers)
        playlist = proxy.replace_proxy_link(adaptive_link, headers=headers, replace_fn=replacement)

    url = PasteBin().dpaste(playlist, name='adaptivestream', expire=60)
    url = proxy.prepend_url(url, '-dl')
    return url, 'png'


def replacement(url):
    if 'googleusercontent.com/gadgets/proxy' in url:
        url = re.search(r'url=(.*)', url).group(1)
        url = unquote(url)

    if 'vdicdn.com' in url:
        url = "{}|{}".format(url, urlencode({
            'referer': 'https://fim1080.com/'
        }))

    if 'vdicdn.com' in url:
        url = "{}|{}".format(url, urlencode({
            'referer': 'https://fim1080.com/'
        }))

    return url
