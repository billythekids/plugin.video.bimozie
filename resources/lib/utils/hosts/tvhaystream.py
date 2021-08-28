# -*- coding: utf-8 -*-
import json
import re

from ..mozie_request import Request
from ..pastebin import PasteBin
from .. import proxy_helper as proxy

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def get_link(url, media):
    req = Request()
    # base_url = urlparse(url)
    # base_url = base_url.scheme + '://' + base_url.netloc

    repsonse = req.get(url)
    idfile = re.search(r'idfile\s?=\s?"(.*)";', repsonse).group(1)
    iduser = re.search(r'idUser\s?=\s?"(.*)";', repsonse).group(1)
    base_url = re.search(r"DOMAIN_API\s?=\s?'(.*)';", repsonse).group(1)
    base_url_rd = re.search(r'DOMAIN_LIST_RD\s?=\s?(.*);', repsonse).group(1)

    repsonse = req.post('{}/{}/{}'.format(base_url, iduser, idfile), params={
        'referrer': 'http://tvhai.org',
        'typeend': 'html'
    })

    content = create_playlist(repsonse, iduser, base_url_rd)
    playlist = proxy.replace_proxy_content(content)

    url = PasteBin().dpaste(playlist, name='adaptivestream', expire=60)
    url = proxy.prepend_url(url, '-dl')
    return url, 'tvhaystream'


def create_playlist(text, idfile, domains):
    data = json.loads(text)
    domains = json.loads(domains)

    play_list = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:{}\n#EXT-X-PLAYLIST-TYPE:VOD\n".format(
        data.get('tgdr'))

    j = 0
    for i in range(len(data.get('data')[0])):
        domain = domains[j]
        j += 1
        if j >= len(domains): j = 0
        play_list += "#EXTINF:{},\n".format(data.get('data')[0][i])
        play_list += "https://{}/rdv5/{}/{}/{}.rd\n".format(
            domain,
            data.get('quaity'),
            idfile,
            data.get('data')[1][i]
        )

    play_list += "#EXT-X-ENDLIST"
    return play_list
