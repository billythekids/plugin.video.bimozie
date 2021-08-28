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
    res = Request()
    resp = res.get(url, redirect=False)
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc
    ajax_url = ''

    md5file = re.search('md5file\s?=\s?"(.*?)"', resp).group(1)
    if 'phimmoi.pro' in base_url:
        ajax_url = "{}/v1.0/json/{}".format(base_url, md5file)
    elif 'streamvip.xyz' in base_url:
        ajax_url = "{}/api/json/{}".format(base_url, md5file)

    resp = res.get(ajax_url)
    chunk_lists = json.loads(resp)

    data = chunk_lists.get('content').get('playlist')[0]

    playlist = proxy.replace_proxy_content(build_play_list(data))
    url = PasteBin().dpaste(playlist, name='adaptivestream', expire=60)

    return url, 'png'


def build_master(chunks, url):
    return """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH={},RESOLUTION={}
{}
    """.format(chunks.get('bandwidth'), chunks.get('resolution'), url)


def build_play_list(chunks):
    play_list = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:{}\n#EXT-X-PLAYLIST-TYPE:VOD\n".format(
        chunks.get('duration'))

    for chunk in chunks.get('content'):
        play_list += "#EXTINF:{}\n".format(chunk.get('extinf'))
        play_list += "{}\n".format(chunk.get('url'))

    play_list += "#EXT-X-ENDLIST"

    return play_list
