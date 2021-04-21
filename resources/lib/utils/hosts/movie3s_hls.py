# -*- coding: utf-8 -*-
from ..mozie_request import Request
from ..pastebin import PasteBin
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, movie):
    request = Request()
    response = request.get(url)
    response = response.replace('/redirect/hls', '/hls')

    url = PasteBin().dpaste(response, name='movie3s', expire=60)
    return url, 'movie3s_hls'
