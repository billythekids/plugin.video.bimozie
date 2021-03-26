# -*- coding: utf-8 -*-

import re

from .. import xbmc_helper as helper

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse
from ..mozie_request import Request


def get_link(url):
    helper.log("*********************** Apply animehay url %s" % url)
    req = Request()

    req.get(url, redirect=True)
    response = req.get_request()
    location = response.history[0].headers['Location']

    id = re.search('id=(.*)', location).group(1)
    base_url = urlparse(location)
    base_url = base_url.scheme + '://' + base_url.netloc

    return '%s/hls/%s/%s.playlist.m3u8' % (base_url, id, id)


def create_playlist(data):
    helper.log(data)
