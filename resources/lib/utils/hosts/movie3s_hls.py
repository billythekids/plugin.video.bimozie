# -*- coding: utf-8 -*-
import re, json, base64, xbmcgui
from urlparse import urlparse
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin
from urllib import urlencode


def get_link(url, movie):
    request = Request()
    response = request.get(url)
    response = response.replace('/redirect/hls', '/hls')

    url = PasteBin().dpaste(response, name='movie3s', expire=60)
    return url, 'movie3s_hls'
