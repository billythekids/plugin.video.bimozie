# -*- coding: utf-8 -*-

import json
try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs
from utils.mozie_request import Request
from utils.aes import CryptoAES


def get_link(url):
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
    return url, 'motphim'


def create_playlist(data):
    print(data)
