# -*- coding: utf-8 -*-

import re
from urlparse import urlparse
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin
from urllib import urlencode


def get_link(url, media, parser=False):
    header = {
        'Referer': media.get('originUrl'),
    }

    print "HLS parser: {}".format(url)

    if parser:
        url = get_stream(url, header)
    # return None, None
    return str(url) + "|%s" % urlencode(header), 'hls_parser'


def get_stream(url, header, base_path=None, action="HEAD"):
    req = Request()
    r = req.get(url, headers=header)

    if not base_path:
        base_url = urlparse(url)
        base_url = base_url.scheme + '://' + base_url.netloc
    else:
        base_url= base_path

    if re.search('EXT-X-STREAM-INF', r):
        ad_url = get_adaptive_link(r)
        if 'http' not in ad_url:
            ad_url = base_url + ad_url
        r = req.get(ad_url, headers=header)

    playlist = ""
    links = []
    is_redirect = True
    lines = r.splitlines()
    for line in lines:
        if len(line) > 0:
            # guess link
            if '#' not in line[0]:
                if 'http' in line:
                    path = line
                elif '//' in line[0:2]:
                    path = "{}{}".format("https:", line)
                elif '/' in line[0]:
                    path = "{}/{}".format(base_url, line)
                else:
                    path = "{}/{}".format(base_url, line)

                if 'vdacdn.com' in path:
                    is_redirect = False
                    path = path.replace('https://', 'http://')

                if 'cdnplay.xyz' in path:
                    is_redirect = False

                # path += "|%s" % urlencode(header)
                links.append({'url': path, 'parser': parse_link, 'responseHeader': True})
            else:
                path = line
            playlist += '%s\n' % path

    if is_redirect and len(playlist) > 0:
        arequest = AsyncRequest(request=req)
        results = arequest.get(links, redirect=False, headers=header, verify=False)
        for i in range(len(links)):
            playlist = playlist.replace(links[i].get('url'), results[i])

    url = PasteBin().dpaste(playlist, name='adaptivestream', expire=60)
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
    elif '360' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '360' == i), -1)
        url = matches[idx]
    if '//' in url[0:2]:
        url = "{}{}".format("https:", url)

    return url


def parse_link(response, args, response_headers):
    return response_headers['Location']
