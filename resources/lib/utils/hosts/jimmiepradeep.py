# -*- coding: utf-8 -*-
import re

from .. import proxy_helper as proxy
from ..pastebin import PasteBin

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def get_link(url, media):
    m_id = re.search('id=(.*)', url).group(1)
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    url = "{}/playlist/{}/1".format(base_url, m_id)
    adaptive_link = proxy.get_adaptive_link(url)
    playlist = proxy.replace_proxy_link(adaptive_link)
    url = PasteBin().dpaste(playlist, name='adaptivestream', expire=60)

    return url, 'png'



