# -*- coding: utf-8 -*-
import re, json, base64, xbmcgui
from urlparse import urlparse
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin
from urllib import urlencode
import iframeembed, cors


def get_link(url, movie):
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc
    request = Request()

    if 'embedplay' in url:
        return iframeembed.get_link(url, movie)

    if url.endswith('m3u8'):
        header = {
            'Origin': 'http://www.vtv16.com',
            'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
            'Referer': movie.get('originUrl')
        }
        return url + "|%s" % urlencode(header), base_url

    # method 1
    try:
        mid = re.search(r'\?id=((?:(?!\?).)*)', url).group(1)
        base_url = urlparse(url)
        base_url = base_url.scheme + '://' + base_url.netloc
        url = "%s/hls/%s/%s.playlist.m3u8" % (base_url, mid, mid)

        return cors.get_link(url, movie, including_agent=False)
    except:
        pass

    # method 2
    request.get(url)

    location = request.get_request().history[0].headers['Location']
    base_url = urlparse(location)
    base_url = base_url.scheme + '://' + base_url.netloc

    # https://vip4.movie3s.net/public/dist/index.html?id=0676953662683db3977a8d30e4084414
    mid = re.search(r'\?id=(.*)', location).group(1)

    return '%s/hls/%s/%s.playlist.m3u8' % (base_url, mid, mid), base_url

    # method 3
    medias = json.loads(request.post('%s/vl/%s' % (base_url, mid)))

    if '720p' in medias:
        return create_stream(medias['720p'], base_url)

    return url, base_url
