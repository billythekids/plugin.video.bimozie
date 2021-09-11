# -*- coding: utf-8 -*-

import json

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs
from ..mozie_request import Request
from ..aes import CryptoAES
from six.moves.urllib.parse import unquote
import xbmcgui


def get_link(url, media, link_parser):
    req = Request()
    url = url.replace('motphim.net', 'motphimzzz.com')
    url = url.replace('motphimzzz.com', 'motphjm.net')

    base_url = urlparse(url)

    parsed = urlparse(url)
    response = req.post("https://cloud.mpapis.xyz/api", params={
        'key': parse_qs(parsed.query)['d'][0]
    }, headers={
        'origin': "https://motphjm.net"
    })

    listitems = []
    movie_items = []
    for data in json.loads(response):
        name = unquote(data[0])
        if 'Hydrax' not in name:
            url = CryptoAES().decrypt(data[1], '{}45904818772018'.format(base_url.netloc))
            movie_items.append((url, name))
            listitems.append("%s (%s)" % (name, url))

    selected_item = None
    if len(listitems) > 1:
        index = xbmcgui.Dialog().select("Select stream", listitems)
        if index == -1:
            return None, None
        else:
            selected_item = movie_items[index]

    media['link'] = selected_item[0]
    link_parser.set_media(media)
    return link_parser.get_link()

