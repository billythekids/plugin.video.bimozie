# -*- coding: utf-8 -*-
from urlparse import urlparse, parse_qs
import cors
from urllib import urlencode


def create_master_playlist(url):
    return """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=648224,RESOLUTION=640x360
{}
    """.format(url)


def get_link(url, media):
    print "Apply vanlongstreaming parser"
    base_url = urlparse(url)
    id = parse_qs(base_url.query).get('id')[0]
    base_url = base_url.scheme + '://' + base_url.netloc

    url = '%s/hls/%s/%s.playlist.m3u8' % (base_url, id, id)
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SAMSUNG SM-N960F Build/M1AJQ) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/8.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
        'Origin': base_url,
        'verifypeer': 'false'
    }
    return url + "|%s" % urlencode(header), 'vanlong'

    return cors.get_link(url, media, True)
