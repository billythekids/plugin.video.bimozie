# -*- coding: utf-8 -*-
import base64

import xbmcaddon

try:
    from urllib.parse import urlencode
except ImportError:
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
        'user-agent': "Chrome/59.0.3071.115 Safari/537.36",
        'Referer': movie.get('originUrl')
    }

    return url + "|%s" % urlencode(header), 'hls5'
