# -*- coding: utf-8 -*-
import re
import json
import math
import utils.xbmc_helper as helper
from urlparse import urlparse
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin
from urllib import urlencode


def get_link(url, media):
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc
    header = {
        'Origin': base_url,
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
    }
    request = Request(header)

    response = request.get(str(url))

    resolutions = re.findall('RESOLUTION=\d+x(\d+)', response)
    matches = re.findall(r'(.*\.m3u8)', response)
    print("Found total %d stream" % len(resolutions), resolutions)
    if len(resolutions) > 1:
        if '1080' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
            stream_url = url.replace('playlist.m3u8', matches[idx])
            stream_url = calculate_stream(request.get(stream_url), base_url, media['originUrl'])
            print("1080 url:%s" % stream_url)
            if stream_url:
                return stream_url

        if '720' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
            stream_url = url.replace('playlist.m3u8', matches[idx])
            stream_url = calculate_stream(request.get(stream_url), base_url, media['originUrl'])
            print("720 url:%s" % stream_url)
            if stream_url:
                return stream_url

        if '360' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '360' == i), -1)
            stream_url = url.replace('playlist.m3u8', matches[idx])
            stream_url = calculate_stream(request.get(stream_url), base_url, media['originUrl'])
            print("360 url:%s" % stream_url)
            if stream_url:
                return stream_url

    return str(url) + "|%s" % urlencode(header)


def calculate_stream(content, origin, referer):
    if re.search(r'#EXT-X-KEY:METHOD=AES-128', content):
        return None

    # get all links
    content = content.replace('//immortal.hydrax.net', 'http://immortal.hydrax.net')
    reg = re.findall('(http://immortal.hydrax.net/.*/.*/(.*)/(.*))/.*\n', content)
    if reg:
        ms = list()
        for i in range(len(reg)):
            link = 'http://immortal.hydrax.net/%s/%s' % (reg[i][1], reg[i][2])
            if link not in ms:
                ms.append(link)
            content = content.replace(reg[i][0], link)
    else:
        ms = re.findall('(http://immortal.hydrax.net/.*/.*)/.*\n', content)
        ms = list(dict.fromkeys(ms))

    arequest = AsyncRequest()
    results = arequest.get(ms, headers={
        'Origin': origin,
        'Referer': referer
    })

    max_targetduration = 12
    play_list = "#EXTM3U\n#EXT-X-VERSION:5\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXT-X-TARGETDURATION:12\n#EXT-X-MEDIA-SEQUENCE:0\n"
    hash = re.search("(#EXT-X-KEY.*?)\n", content)
    if hash:
        play_list += hash.group(0)

    for i in range(len(ms)):
        link = ms[i]
        slashlink = link.replace('-', '\\-')
        slashlink = slashlink.replace('*', '\\*')
        slashlink = slashlink.replace('?', '\\?')

        duration = 0
        lengthbyte = 0
        startbyte = 999999999

        segments = re.findall(
            r"(#EXTINF:([0-9]*\.?[0-9]+),\n#EXT-X-BYTERANGE:([0-9]+)@([0-9]+)(?:(?!#EXTINF).)*" + slashlink + ").*?\n",
            content, re.DOTALL)

        for segment in segments:
            duration += float(segment[1])
            startbyte = int(segment[3]) < startbyte and int(segment[3]) or startbyte
            lengthbyte += int(segment[2])

        play_list += "#EXTINF:%s,\n" % duration
        play_list += "#EXT-X-BYTERANGE:%s@%s\n" % (lengthbyte, startbyte)
        play_list += "%s\n" % helper.fixurl(json.loads(results[i])['url'])

        if duration > max_targetduration:
            max_targetduration = duration

    play_list = play_list.replace("TARGETDURATION:12", "TARGETDURATION:" + str(int(math.ceil(max_targetduration))))
    play_list += "#EXT-X-ENDLIST\n"

    url = PasteBin().dpaste(play_list, name=referer, expire=60)
    return url
