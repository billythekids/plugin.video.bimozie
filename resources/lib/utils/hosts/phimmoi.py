# -*- coding: utf-8 -*-
import re
import urllib
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin


def get_link(url, originURL):
    url += '|referer=' + urllib.quote_plus(originURL)
    return url, 'Phimmoi HLS'


def get_link_deprecated(url, originURL):
    req = Request()
    response = req.get(url)

    # found playlist
    if re.search('EXT-X-STREAM-INF', response):
        resolutions = re.findall('RESOLUTION=\d+x(\d+)', response)
        matches = re.findall('(http.*)\r', response)
        if '1080' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '1080' == i), -1)
            url = matches[idx]
        elif '720' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
            url = matches[idx]
        elif '480' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '480' == i), -1)
            url = matches[idx]

        response = Request().get(url, headers={
            'origin': 'http://www.phimmoi.net'
        })

    links = re.findall('(https?://(?!so-trym).*)\r', response)
    if links:
        media_type = 'hls4'
        arequest = AsyncRequest(request=req, retry=2)
        results = arequest.head(links, headers={
            'origin': 'http://www.phimmoi.net',
            'referer': originURL
        }, redirect=False)

        for i in range(len(links)):
            try:
                response = response.replace(links[i], results[i].headers['location'])
            except:
                print(links[i], results[i].headers)
    else:
        media_type = 'hls3'

    stream_url = PasteBin().dpaste(response, name=url, expire=60)
    playlist = "#EXTM3U\n#EXT-X-VERSION:3\n"
    playlist += "#EXT-X-STREAM-INF:BANDWIDTH=3998000,RESOLUTION=9999x9999\n"
    playlist += "%s\n" % stream_url
    url = PasteBin().dpaste(playlist, name=url, expire=60)
    if 'hls' == media_type:
        url += '|referer=' + urllib.quote_plus(originURL)

    return url, media_type
