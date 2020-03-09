# -*- coding: utf-8 -*-
import xbmcaddon
import base64
from urllib import urlencode


def get_link(url, movie):
    try:
        if xbmcaddon.Addon(id='service.liveproxy'):
            command = 'streamlink --player-passthrough=http,hls,rtmp --http-header "Origin=%s" %s best' % (
            movie.get('originUrl'), url)
            return "http://127.0.0.1:53422/base64/%s" % base64.b64encode(command), 'hls5'
    except:
        pass

    header = {
        'Origin': movie.get('originUrl'),
        'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
        'Referer': movie.get('originUrl')
    }

    return url + "|%s" % urlencode(header), 'hls5'
