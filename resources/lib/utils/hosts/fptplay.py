# -*- coding: utf-8 -*-
import re

from .. import xbmc_helper as helper
from six.moves.urllib.parse import unquote
from ..mozie_request import Request
from ..pastebin import PasteBin

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url):
    helper.log("*********************** Apply fptplay url %s" % url)
    header = {
        'Origin': 'https://fptplay.vn',
        'user-agent':  "Chrome/59.0.3071.115 Safari/537.36"
    }
    return str(url) + "|%s" % urlencode(header), 'hls3'

    return url, 'hls3'
    r = re.search('streamFPT\?url=(.*)', url)
    if r:
        url = unquote(r.group(1))

    base_url = url.rpartition('/')[0]
    response = Request().get(url)

    matches = re.findall('(chunklist.*)', response)

    for m in matches:
        stream_url = base_url + '/' + m
        response = response.replace(m, __get_fptplay_stream(stream_url, base_url))

    url = PasteBin().dpaste(response, name=url, expire=60)
    return url, 'hls3'


def __get_fptplay_stream(url, base_url):
    response = Request().get(url)
    matches = re.findall('(media_.*)', response)

    for m in matches:
        stream_url = base_url + '/' + m
        response = response.replace(m, stream_url)

    url = PasteBin().dpaste(response, name=url, expire=60)
    return url
