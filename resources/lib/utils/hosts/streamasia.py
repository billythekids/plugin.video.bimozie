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
    url = "{}/hls/{}/{}?v=1626430620868".format('https://streamasia.cloud', m_id, m_id)
    playlist = proxy.replace_proxy_link(url)
    return PasteBin().dpaste(playlist, name='adaptivestream', expire=60), 'manga123'
