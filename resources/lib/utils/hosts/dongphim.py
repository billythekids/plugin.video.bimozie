# -*- coding: utf-8 -*-

import re

import utils.xbmc_helper as helper
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, media):
    helper.log("*********************** Apply dongphim url %s" % url)
    header = {
        'Origin': 'http://dongphim.net'
    }

    # url = get_stream(url)
    return str(url) + "|%s" % urlencode(header), 'dongphim'


def get_stream(url):
    req = Request()
    r = req.get(url)
    if re.search('EXT-X-STREAM-INF', r):
        return url

    str = ""
    links = []
    for line in r.splitlines():
        if len(line) > 0:
            if re.match('http', line):
                links.append(line)
            str += '%s\n' % line

    arequest = AsyncRequest(request=req)
    results = arequest.head(links)
    for i in range(len(links)):
        try:
            str = str.replace(links[i], results[i].headers['Location '])
        except:
            pass

    url = PasteBin().dpaste(str, name='dongphim', expire=60)
    return url
