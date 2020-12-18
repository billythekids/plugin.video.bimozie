# -*- coding: utf-8 -*-
import xbmcaddon
import base64, json
from urllib import urlencode


def get_link(url, movie, headers=None):
    try:
        if xbmcaddon.Addon(id='service.liveproxy'):
            if headers:
                command = 'streamlink --player-passthrough=http,hls,rtmp'
                
            elif movie.get('originUrl'):
                command = 'streamlink --player-passthrough=http,hls,rtmp --http-header "Origin=%s" --http-header "Referer=%s" %s best' % (
                movie.get('originUrl'), movie.get('originUrl'), url)
            else:
                command = 'streamlink --player-passthrough=http,hls,rtmp %s best' % (url)
            return "http://127.0.0.1:53422/base64/%s" % base64.b64encode(command), 'hls5'
    except:
        pass

    header = {
        'Origin': movie.get('originUrl'),
        'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
        'Referer': movie.get('originUrl')
    }

    return url + "|%s" % urlencode(header), 'wowza'
