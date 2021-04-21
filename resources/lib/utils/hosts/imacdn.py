# -*- coding: utf-8 -*-
import re

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from ..mozie_request import Request
from ..pastebin import PasteBin
from .. import xbmc_helper as helper


def get_link(url, media):
    header = {
        'Referer': media.get('originUrl'),
        'Origin': 'https://fimfast.com',
        'user-agent': "Chrome/59.0.3071.115 Safari/537.36"
    }
    return url + "|%s" % urlencode(header)

    play_list = ""
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc
    resp = Request().get(url)
    resolutions = re.findall('RESOLUTION=\d+x(\d+)', resp)
    matches = re.findall('(/[a-zA-z]+/.*)', resp)

    if len(resolutions) > 1:
        play_list += "#EXTM3U\n"
        if '2048' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '1080' == i), -1)
            url = matches[idx]
            stream_url = base_url + url
            return stream_url + "|%s" % urlencode(header)
        elif '1080' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '1080' == i), -1)
            url = matches[idx]
            stream_url = base_url + url
            return stream_url + "|%s" % urlencode(header)
            return create_imacdn_stream(stream_url, base_url)
            # play_list += "#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1920x1080\n"
            # play_list += "%s\n" % create_imacdn_stream(stream_url, base_url)
        elif '720' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
            url = matches[idx]
            stream_url = base_url + url
            return stream_url + "|%s" % urlencode(header)
            return create_imacdn_stream(stream_url, base_url)
            # play_list += "#EXT-X-STREAM-INF:BANDWIDTH=1500000,RESOLUTION=1280x720\n"
            # play_list += "%s\n" % create_imacdn_stream(stream_url, base_url)
        elif '480' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '480' == i), -1)
            url = matches[idx]
            stream_url = base_url + url
            return stream_url + "|%s" % urlencode(header)
            return create_imacdn_stream(stream_url, base_url)
            # play_list += "#EXT-X-STREAM-INF:BANDWIDTH=750000,RESOLUTION=854x480\n"
            # play_list += "%s\n" % create_imacdn_stream(stream_url, base_url)
    else:
        play_list = resp
        for m in matches:
            stream_url = base_url + m
            play_list = play_list.replace(m, create_imacdn_stream(stream_url, base_url))

    url = PasteBin().dpaste(play_list, name=url, expire=60)
    return url


def create_imacdn_stream(url, base_url):
    retry = 5
    res = Request()
    response = None
    while retry >= 0:
        try:
            helper.log('Retry %d' % retry)
            response = res.get(url)
            if response != 'error': break
        except:
            pass
        finally:
            retry -= 1

    if response:
        matches = re.findall('(/drive/hls/.*)', response)
        for m in matches:
            stream_url = base_url + m
            response = response.replace(m, stream_url)
        url = PasteBin().dpaste(response, name=url, expire=60)
    helper.log("------------------------------------ %s") % url
    return url
