# -*- coding: utf-8 -*-
import json
import re

from cloudscraper2 import CloudScraper

from .. import proxy_helper as proxy
from ..mozie_request import Request
from ..pastebin import PasteBin

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, media):
    req = Request()
    # base_url = urlparse(url)
    # base_url = base_url.scheme + '://' + base_url.netloc

    repsonse = req.get(url)
    idfile = re.search(r'idfile\s?=\s?"(.*)";', repsonse).group(1)
    iduser = re.search(r'idUser\s?=\s?"(.*)";', repsonse).group(1)
    base_url = re.search(r"DOMAIN_API\s?=\s?'(.*)';", repsonse).group(1)
    base_url_rd = re.search(r'DOMAIN_LIST_RD\s?=\s?(.*);', repsonse).group(1)

    # https://apiif-tvhai.rdgogo.xyz/apiv3/5ee31dd5665f2d19d5af4a99/613ae0981e2bd95dcf60e2f1
    # https://apiif-tvhai.rdgogo.xyz/apiv3/5ee31dd5665f2d19d5af4a99/613ae0981e2bd95dcf60e2f1

    tmp_url = '{}{}/{}'.format(base_url, iduser, idfile)

    scraper = CloudScraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }, allow_brotli=False)
    scraper.headers.update({
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.8',
    })
    response = scraper.post(tmp_url,
        data={
            'referrer': 'http://tvhai.org',
            'typeend': 'html'
        })

    content = create_playlist(response.text, iduser, base_url_rd)
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

        play_list += "https://{}/stream/v5/{}.html|{}\n".format(
            domain,
            data.get('data')[1][i],
            urlencode({
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
                'origin': 'https://play.tvhaystream.xyz'
            })
        )

    play_list += "#EXT-X-ENDLIST"
    return play_list
