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

    parsed = urlparse(url)
    response = req.post("https://iapi.mpapis.xyz/cloud/", params={
        'd': parse_qs(parsed.query)['d']
    }, headers={
        'origin': "https://motphimzzz.com"
    })
    url = CryptoAES().decrypt(json.loads(response).get('d'), 'motphimzzz.com45904818772018')
    return url, 'motphim'


def create_playlist(data):
    print(data)
