# -*- coding: utf-8 -*-
import re

from .. import proxy_helper as proxy
from ..pastebin import PasteBin
from six.moves.urllib.parse import unquote

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def get_link(url, media):
    adaptive_link = proxy.get_adaptive_link(url)
    playlist = proxy.replace_proxy_link(adaptive_link, replace_fn=replacement)
    # playlist = proxy.replace_proxy_link(adaptive_link)
    print(playlist)
    # return None, None

    url = PasteBin().dpaste(playlist, name='adaptivestream', expire=60)
    url = proxy.prepend_url(url, '-dl')
    return url, 'png'


def replacement(url):
    if 'googleusercontent.com/gadgets/proxy' in url:
        url = re.search(r'url=(.*)', url).group(1)
        url = unquote(url)

    return url
