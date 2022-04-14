# -*- coding: utf-8 -*-
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
from ..mozie_request import Request
import json


def get_link(url, media):
    helper.log("Apply GOTPHIM parser")
    base_url = urlparse(url)
    m_id = parse_qs(base_url.query).get('id')[0]
    base_url = base_url.scheme + '://' + base_url.netloc

    # https://play.gotphim.com/iframe/video/6129aecd13c48c06d44cdaf5
    # https://play.gotphim.com/cdn01/hls/6129aecd13c48c06d44cdaf5/main.m3u8
    url = '%s/player/%s/playlist.m3u8' % (base_url, m_id)
    headers = header = {
        'Origin': base_url,
    }

    content = Request().get(url, headers=headers)
    print(content)
    return None, None

    # content = json.loads(Request().post(url, headers=headers))
    # part_url = content.get('data').get('url')
    # url = '%s%s' % (base_url, part_url)
    # base_url = 'https://flash.imgtv.club{}'.format(part_url.replace('/main.m3u8', ''))
    # playlist = proxy.replace_proxy_content(Request().get(url), base_url)
    # url = PasteBin().dpaste(playlist, name='adaptivestream', expire=60)
    # url = proxy.prepend_url(url, '-dl')
    return url, 'gotphim'
