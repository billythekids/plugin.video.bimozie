# -*- coding: utf-8 -*-

import re
from urlparse import urlparse
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin
from urllib import urlencode


def get_link(url, media):
    header = {
        'Referer': media.get('originUrl'),
    }

    url = get_stream(url, header)
    # return None, None
    return str(url) + "|%s" % urlencode(header), 'm3u8'


def get_stream(url, header):
    req = Request()
    r = req.get(url, headers=header)

    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    if re.search('EXT-X-STREAM-INF', r):
        ad_url = get_adaptive_link(r, req, base_url, header)
        if 'http' not in ad_url:
            ad_url = base_url + ad_url
        r = req.get(ad_url, headers=header)

    playlist = ""
    links = []
    is_redirect = True
    for line in r.splitlines():
        if len(line) > 0:
            # guess link
            if line[0] not in '#':
                if re.match('http', line):
                    path = line
                else:
                    path = "{}{}".format(base_url, line)

                if 'vdacdn.com' in path:
                    is_redirect = False
                    path = path.replace('https://', 'http://')

                # path += "|%s" % urlencode(header)
                links.append({'url': path, 'parser': parse_link, 'responseHeader': True})
            else:
                path = line

            playlist += '%s\n' % path

    if is_redirect and len(playlist) > 0:
        arequest = AsyncRequest(request=req)
        results = arequest.get(links, redirect=False, headers=header)
        for i in range(len(links)):
            playlist = playlist.replace(links[i].get('url'), results[i])

    url = PasteBin().dpaste(playlist, name='dongphim', expire=60)
    return url


def get_adaptive_link(response):
    resolutions = re.findall(r'RESOLUTION=\d+x(\d+)', response)
    matches = re.findall(r'^(?!#)(.*)', response, re.MULTILINE)
    if '1080' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '1080' == i), -1)
        url = matches[idx]
    if '1080' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '1080' == i), -1)
        url = matches[idx]
    elif '720' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
        url = matches[idx]
    elif '480' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '480' == i), -1)
        url = matches[idx]

    return url


def parse_link(response, args, response_headers):
    return response_headers['Location']
