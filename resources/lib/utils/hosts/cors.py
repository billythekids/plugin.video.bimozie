# -*- coding: utf-8 -*-

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
from .. import xbmc_helper as helper

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, media, including_agent=True):
    helper.log("Apply CORS url %s - %s" % (media.get('originUrl'), url))
    if media.get('originUrl'):
        base_url = urlparse(media.get('originUrl'))
        base_url = base_url.scheme + '://' + base_url.netloc
        host_url = urlparse(url)

        header = {
            'Referer': media.get('originUrl'),
            'Origin': base_url,
            'verifypeer': 'false'
        }

        if 'cdnproxy.xyz' in url:
            header = {
                'Referer': base_url,
                'Origin': base_url,
                'verifypeer': 'false'
            }

        if including_agent:
            header['user-agent'] = "Chrome/59.0.3071.115 Safari/537.36"

        return url + "|%s" % urlencode(header), "CORS"
    return url, 'CORS'
