# -*- coding: utf-8 -*-

import json
try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs
from ..mozie_request import Request
from ..aes import CryptoAES
from .. import xbmc_helper as helper
from . import vidsugar


def get_link(url, media):
    req = Request()
    url = url.replace('motphim.net', 'motphimzzz.com')
    url = url.replace('motphimzzz.com', 'motphjm.net')

    base_url = urlparse(url)

    parsed = urlparse(url)
    response = req.post("https://iapi.mpapis.xyz/cloud/", params={
        'd': parse_qs(parsed.query)['d']
    }, headers={
        'origin': "https://motphjm.net"
    })
    url = CryptoAES().decrypt(json.loads(response).get('d'), '{}45904818772018'.format(base_url.netloc))

    if 'vidsugar.com' in url:
        return vidsugar.get_link(url, media)

    return url, 'motphim'


def create_playlist(data):
    helper.log(data)
